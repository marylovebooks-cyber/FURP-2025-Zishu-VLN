# Week 3 Report: Minimal Language-to-Waypoint Baseline

## Goal

The goal of Week 3 was to create a small baseline that connects language input
to a robot-executable navigation target.

## Baseline

The baseline uses a simple rule-based method:

1. Load a toy landmark map.
2. Read natural-language instructions from a CSV file.
3. Match each instruction to a known landmark by name.
4. Export a structured goal pose with `x`, `y`, and `theta`.

Supporting files:

- `src/week03_baseline/README.md`
- `src/week03_baseline/landmarks.json`
- `src/week03_baseline/sample_instructions.csv`
- `src/week03_baseline/language_to_waypoint.py`
- `src/week03_baseline/outputs/week03_language_to_waypoint_results.csv`

## Command

From `src/week03_baseline`:

```bash
python3 language_to_waypoint.py
```

## Result

The sample evaluation contains four simple instructions:

| Instruction | Expected landmark |
|---|---|
| go to the lab entrance | lab entrance |
| move to the blue poster | blue poster |
| navigate to the charging station | charging station |
| go to the meeting table | meeting table |

Because the initial instructions directly mention the landmark names, the
baseline is expected to match all four examples. This is intentionally simple:
the purpose is to define the interface between language interpretation and robot
navigation.

## Importance

This baseline does not solve full VLN. Its value is that it creates a concrete
intermediate representation:

```json
{"target":"blue poster","frame_id":"map","pose":{"x":2.4,"y":1.2,"theta":1.57}}
```

This representation can be passed to a ROS 2/Nav2-style navigation system in
Week 4.

## Limitations

- It only supports exact landmark mentions.
- It does not understand multi-step instructions.
- It does not use camera observations.
- The map is a toy map, not yet a real simulator or AMR map.

## Next Step

Week 4 should focus on the AMR interface study: confirm the native Ubuntu 22.04
ROS 2 environment, check Nav2/TurtleBot3/Gazebo availability, and connect the
generated goal pose to a navigation execution or simulator test.
