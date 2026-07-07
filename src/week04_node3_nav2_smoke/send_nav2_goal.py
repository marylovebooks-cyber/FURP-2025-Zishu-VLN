#!/usr/bin/env python3
"""Send one fixed TurtleBot3 Nav2 goal and save smoke-test evidence."""

from __future__ import annotations

import argparse
import csv
import math
import time
from pathlib import Path

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal-x", type=float, default=1.0)
    parser.add_argument("--goal-y", type=float, default=0.5)
    parser.add_argument("--goal-yaw", type=float, default=0.0)
    parser.add_argument("--initial-x", type=float, default=0.0)
    parser.add_argument("--initial-y", type=float, default=0.0)
    parser.add_argument("--initial-yaw", type=float, default=0.0)
    parser.add_argument("--timeout-sec", type=float, default=180.0)
    parser.add_argument("--output", type=Path, default=Path("outputs/nav2_goal_result.csv"))
    args = parser.parse_args()

    rclpy.init()
    navigator = BasicNavigator()

    navigator.setInitialPose(
        make_pose(navigator, args.initial_x, args.initial_y, args.initial_yaw)
    )
    navigator.waitUntilNav2Active()

    goal = make_pose(navigator, args.goal_x, args.goal_y, args.goal_yaw)
    start_time = time.monotonic()
    navigator.goToPose(goal)

    last_feedback_distance = ""
    while not navigator.isTaskComplete():
        elapsed = time.monotonic() - start_time
        feedback = navigator.getFeedback()
        if feedback is not None and hasattr(feedback, "distance_remaining"):
            last_feedback_distance = f"{feedback.distance_remaining:.3f}"
        if elapsed > args.timeout_sec:
            navigator.cancelTask()
            break
        time.sleep(0.5)

    elapsed = time.monotonic() - start_time
    result = navigator.getResult()
    result_name = task_result_name(result)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "initial_x",
                "initial_y",
                "initial_yaw",
                "goal_x",
                "goal_y",
                "goal_yaw",
                "timeout_sec",
                "duration_sec",
                "nav2_result",
                "last_feedback_distance_m",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "initial_x": args.initial_x,
                "initial_y": args.initial_y,
                "initial_yaw": args.initial_yaw,
                "goal_x": args.goal_x,
                "goal_y": args.goal_y,
                "goal_yaw": args.goal_yaw,
                "timeout_sec": args.timeout_sec,
                "duration_sec": f"{elapsed:.3f}",
                "nav2_result": result_name,
                "last_feedback_distance_m": last_feedback_distance,
            }
        )

    navigator.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
