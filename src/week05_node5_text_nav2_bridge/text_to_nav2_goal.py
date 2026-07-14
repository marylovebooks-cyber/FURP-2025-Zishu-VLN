#!/usr/bin/env python3
"""Parse text instructions into TurtleBot3 Nav2 goals and execute them."""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


@dataclass(frozen=True)
class Landmark:
    name: str
    aliases: tuple[str, ...]
    x: float
    y: float
    theta: float


def load_landmarks(path: Path) -> list[Landmark]:
    with path.open("r", encoding="utf-8") as file:
        raw: dict[str, dict[str, Any]] = json.load(file)

    landmarks = []
    for name, pose in raw.items():
        aliases = tuple(str(alias).lower() for alias in pose.get("aliases", []))
        if not aliases:
            aliases = (name.lower(),)
        landmarks.append(
            Landmark(
                name=name,
                aliases=aliases,
                x=float(pose["x"]),
                y=float(pose["y"]),
                theta=float(pose["theta"]),
            )
        )
    return landmarks


def match_landmark(instruction: str, landmarks: list[Landmark]) -> Landmark | None:
    text = instruction.lower()
    # Prefer longer aliases so "center upper left" wins before "center".
    candidates = sorted(
        ((alias, landmark) for landmark in landmarks for alias in landmark.aliases),
        key=lambda item: len(item[0]),
        reverse=True,
    )
    for alias, landmark in candidates:
        if alias in text:
            return landmark
    return None


def set_yaw(pose, yaw: float) -> None:
    pose.orientation.z = math.sin(yaw / 2.0)
    pose.orientation.w = math.cos(yaw / 2.0)


def make_pose(navigator: BasicNavigator, x: float, y: float, yaw: float) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    set_yaw(pose.pose, yaw)
    return pose


def task_result_name(result: TaskResult) -> str:
    if result == TaskResult.SUCCEEDED:
        return "SUCCEEDED"
    if result == TaskResult.CANCELED:
        return "CANCELED"
    if result == TaskResult.FAILED:
        return "FAILED"
    return str(result)


def run_goal(
    navigator: BasicNavigator,
    landmark: Landmark,
    timeout_sec: float,
) -> dict[str, object]:
    start_time = time.monotonic()
    navigator.goToPose(make_pose(navigator, landmark.x, landmark.y, landmark.theta))

    feedback_count = 0
    last_feedback_distance = ""
    min_feedback_distance = ""
    timed_out = False

    while not navigator.isTaskComplete():
        elapsed = time.monotonic() - start_time
        feedback = navigator.getFeedback()
        if feedback is not None and hasattr(feedback, "distance_remaining"):
            feedback_count += 1
            distance = float(feedback.distance_remaining)
            last_feedback_distance = f"{distance:.3f}"
            if min_feedback_distance == "" or distance < float(min_feedback_distance):
                min_feedback_distance = f"{distance:.3f}"
        if elapsed > timeout_sec:
            timed_out = True
            navigator.cancelTask()
            break
        time.sleep(0.5)

    result_name = task_result_name(navigator.getResult())
    return {
        "duration_sec": f"{time.monotonic() - start_time:.3f}",
        "nav2_result": result_name,
        "nav2_success": result_name == "SUCCEEDED",
        "timed_out": timed_out,
        "feedback_count": feedback_count,
        "last_feedback_distance_m": last_feedback_distance,
        "min_feedback_distance_m": min_feedback_distance,
    }


def read_instructions(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "trial_id",
        "instruction",
        "expected_landmark",
        "parsed_landmark",
        "parse_success",
        "goal_x",
        "goal_y",
        "goal_yaw",
        "timeout_sec",
        "duration_sec",
        "nav2_result",
        "nav2_success",
        "timed_out",
        "feedback_count",
        "last_feedback_distance_m",
        "min_feedback_distance_m",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--landmarks", type=Path, default=Path("landmarks.json"))
    parser.add_argument("--instructions", type=Path, default=Path("sample_text_nav2_instructions.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/week05_text_to_nav2_results.csv"))
    parser.add_argument("--initial-x", type=float, default=-2.0)
    parser.add_argument("--initial-y", type=float, default=-0.5)
    parser.add_argument("--initial-yaw", type=float, default=0.0)
    parser.add_argument("--timeout-sec", type=float, default=120.0)
    parser.add_argument("--settle-sec", type=float, default=1.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    landmarks = load_landmarks(args.landmarks)
    instructions = read_instructions(args.instructions)

    navigator = None
    if not args.dry_run:
        rclpy.init()
        navigator = BasicNavigator()
        navigator.setInitialPose(
            make_pose(navigator, args.initial_x, args.initial_y, args.initial_yaw)
        )
        navigator.waitUntilNav2Active()

    rows: list[dict[str, object]] = []
    try:
        for instruction_row in instructions:
            instruction = instruction_row["instruction"]
            expected = instruction_row.get("expected_landmark", "")
            landmark = match_landmark(instruction, landmarks)
            parse_success = bool(landmark and landmark.name == expected)

            base_row: dict[str, object] = {
                "trial_id": instruction_row.get("trial_id", ""),
                "instruction": instruction,
                "expected_landmark": expected,
                "parsed_landmark": landmark.name if landmark else "",
                "parse_success": parse_success,
                "goal_x": f"{landmark.x:.3f}" if landmark else "",
                "goal_y": f"{landmark.y:.3f}" if landmark else "",
                "goal_yaw": f"{landmark.theta:.3f}" if landmark else "",
                "timeout_sec": args.timeout_sec,
                "duration_sec": "",
                "nav2_result": "DRY_RUN" if args.dry_run and landmark else "PARSE_FAILED",
                "nav2_success": False,
                "timed_out": False,
                "feedback_count": "",
                "last_feedback_distance_m": "",
                "min_feedback_distance_m": "",
            }

            if landmark and not args.dry_run:
                assert navigator is not None
                base_row.update(run_goal(navigator, landmark, args.timeout_sec))
                time.sleep(args.settle_sec)

            rows.append(base_row)
    finally:
        write_rows(args.output, rows)
        if navigator is not None:
            navigator.lifecycleShutdown()
            rclpy.shutdown()

    nav_successes = sum(1 for row in rows if row["nav2_success"])
    parse_successes = sum(1 for row in rows if row["parse_success"])
    print(f"text parse: {parse_successes}/{len(rows)}")
    if args.dry_run:
        print("dry run complete")
    else:
        print(f"text-to-nav2 execution: {nav_successes}/{len(rows)} succeeded")
    print(f"results: {args.output}")


if __name__ == "__main__":
    main()
