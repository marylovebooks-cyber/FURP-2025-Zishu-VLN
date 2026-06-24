#!/usr/bin/env python3
"""Minimal language-to-waypoint baseline for VLN-AMR integration."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_landmarks(path: Path) -> dict[str, dict[str, float]]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def match_landmark(instruction: str, landmarks: dict[str, dict[str, float]]) -> str | None:
    text = instruction.lower()
    for name in landmarks:
        if name in text:
            return name
    return None


def nav2_goal(landmark: str, pose: dict[str, float]) -> dict[str, object]:
    return {
        "target": landmark,
        "frame_id": "map",
        "pose": {
            "x": pose["x"],
            "y": pose["y"],
            "theta": pose["theta"],
        },
    }


def run_batch(landmarks_path: Path, instructions_path: Path, output_path: Path) -> None:
    landmarks = load_landmarks(landmarks_path)
    rows: list[dict[str, object]] = []

    with instructions_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            instruction = row["instruction"]
            expected = row.get("expected_landmark", "")
            predicted = match_landmark(instruction, landmarks)
            success = predicted == expected
            goal = nav2_goal(predicted, landmarks[predicted]) if predicted else None
            rows.append(
                {
                    "instruction": instruction,
                    "expected_landmark": expected,
                    "predicted_landmark": predicted or "",
                    "success": success,
                    "nav2_goal_json": json.dumps(goal, separators=(",", ":")) if goal else "",
                }
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        fieldnames = [
            "instruction",
            "expected_landmark",
            "predicted_landmark",
            "success",
            "nav2_goal_json",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--landmarks", type=Path, default=Path("landmarks.json"))
    parser.add_argument("--instructions", type=Path, default=Path("sample_instructions.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/week03_language_to_waypoint_results.csv"))
    args = parser.parse_args()
    run_batch(args.landmarks, args.instructions, args.output)


if __name__ == "__main__":
    main()
