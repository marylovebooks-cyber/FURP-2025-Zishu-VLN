#!/usr/bin/env python3
"""Run a 10-goal TurtleBot3 Nav2 benchmark and save CSV evidence."""

from __future__ import annotations

import argparse
import csv
import math
import time
from dataclasses import dataclass
from pathlib import Path

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


@dataclass(frozen=True)
class Goal:
    trial_id: int
    label: str
    x: float
    y: float
    yaw: float = 0.0


GOALS = [
    Goal(1, "center_approach", -1.50, -0.50, 0.0),
    Goal(2, "left_to_center_line", -1.00, -0.50, 0.0),
    Goal(3, "near_center_left", -0.50, -0.50, 0.0),
    Goal(4, "center_lower", 0.00, -0.50, 0.0),
    Goal(5, "map_center", 0.00, 0.00, 0.0),
    Goal(6, "center_upper_left", -0.50, 0.00, 0.0),
    Goal(7, "upper_left", -1.00, 0.00, 0.0),
    Goal(8, "upper_spawn_side", -1.50, 0.00, 0.0),
    Goal(9, "near_spawn_upper", -2.00, 0.00, 0.0),
    Goal(10, "return_spawn", -2.00, -0.50, 0.0),
]


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


def run_goal(navigator: BasicNavigator, goal: Goal, timeout_sec: float) -> dict[str, object]:
    pose = make_pose(navigator, goal.x, goal.y, goal.yaw)
    start_time = time.monotonic()
    navigator.goToPose(pose)

    last_feedback_distance = ""
    min_feedback_distance = ""
    feedback_count = 0
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

    elapsed = time.monotonic() - start_time
    result = navigator.getResult()
    result_name = task_result_name(result)

    return {
        "trial_id": goal.trial_id,
        "label": goal.label,
        "goal_x": goal.x,
        "goal_y": goal.y,
        "goal_yaw": goal.yaw,
        "timeout_sec": timeout_sec,
        "duration_sec": f"{elapsed:.3f}",
        "nav2_result": result_name,
        "success": result_name == "SUCCEEDED",
        "timed_out": timed_out,
        "feedback_count": feedback_count,
        "last_feedback_distance_m": last_feedback_distance,
        "min_feedback_distance_m": min_feedback_distance,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial-x", type=float, default=-2.0)
    parser.add_argument("--initial-y", type=float, default=-0.5)
    parser.add_argument("--initial-yaw", type=float, default=0.0)
    parser.add_argument("--timeout-sec", type=float, default=120.0)
    parser.add_argument("--settle-sec", type=float, default=1.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/nav2_10_goal_benchmark.csv"),
    )
    args = parser.parse_args()

    rclpy.init()
    navigator = BasicNavigator()

    navigator.setInitialPose(
        make_pose(navigator, args.initial_x, args.initial_y, args.initial_yaw)
    )
    navigator.waitUntilNav2Active()

    rows = []
    for goal in GOALS:
        rows.append(run_goal(navigator, goal, args.timeout_sec))
        time.sleep(args.settle_sec)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "trial_id",
        "label",
        "goal_x",
        "goal_y",
        "goal_yaw",
        "timeout_sec",
        "duration_sec",
        "nav2_result",
        "success",
        "timed_out",
        "feedback_count",
        "last_feedback_distance_m",
        "min_feedback_distance_m",
    ]
    with args.output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    successes = sum(1 for row in rows if row["success"])
    print(f"10-goal benchmark complete: {successes}/{len(rows)} succeeded")
    print(f"results: {args.output}")

    navigator.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
