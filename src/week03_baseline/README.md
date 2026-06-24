# Week 3 Baseline: Language to Waypoint

## Purpose

This is a minimal baseline for the AMR integration path:

> natural-language instruction -> landmark match -> goal pose.

It does not solve full VLN. Instead, it creates a small, testable interface that
can later be connected to ROS 2 Nav2.

## Files

| File | Purpose |
|---|---|
| `landmarks.json` | Toy map of named landmarks and poses. |
| `sample_instructions.csv` | Small evaluation set. |
| `language_to_waypoint.py` | Rule-based baseline. |
| `outputs/week03_language_to_waypoint_results.csv` | Generated results. |

## Command

Run from this folder:

```bash
python3 language_to_waypoint.py
```

Expected output:

```text
outputs/week03_language_to_waypoint_results.csv
```

## Result Summary

The current sample set uses direct landmark mentions, so the baseline should
match all four examples. This is intentionally simple. Its value is that the
output already has the shape needed by a Nav2-style goal interface:

```json
{"target":"blue poster","frame_id":"map","pose":{"x":2.4,"y":1.2,"theta":1.57}}
```

## Next Step

In Week 4, replace the toy landmark map with poses from a simulator or AMR map,
then send the generated goal to a ROS 2/Nav2 navigation action.
