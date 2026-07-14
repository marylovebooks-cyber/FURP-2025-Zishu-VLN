# Week 5 / Node 5 Minimal Text-to-Nav2 Bridge

## Purpose

This folder records a small Node 5 bridge:

```text
text instruction -> landmark coordinate -> Nav2 goal -> TurtleBot3 movement
```

It does not use Qwen or live camera input yet. The text parser is rule-based so
the experiment can focus on whether parsed coordinates can be executed by Nav2.

## Files

```text
landmarks.json
sample_text_nav2_instructions.csv
text_to_nav2_goal.py
outputs/week05_text_to_nav2_results.csv
```

The landmarks are TurtleBot3 world coordinates that were already used in the
Week 4 10-goal Nav2 run.

## Dry Run

Check text parsing without Nav2:

```bash
/usr/bin/python3 src/week05_node5_text_nav2_bridge/text_to_nav2_goal.py \
  --landmarks src/week05_node5_text_nav2_bridge/landmarks.json \
  --instructions src/week05_node5_text_nav2_bridge/sample_text_nav2_instructions.csv \
  --output src/week05_node5_text_nav2_bridge/outputs/week05_text_parse_dry_run.csv \
  --dry-run
```

## Online Run

Start Gazebo and Nav2 with the same commands used in Week 4, then run:

```bash
/usr/bin/python3 src/week05_node5_text_nav2_bridge/text_to_nav2_goal.py \
  --landmarks src/week05_node5_text_nav2_bridge/landmarks.json \
  --instructions src/week05_node5_text_nav2_bridge/sample_text_nav2_instructions.csv \
  --initial-x -2.0 \
  --initial-y -0.5 \
  --initial-yaw 0.0 \
  --timeout-sec 120 \
  --settle-sec 1.0 \
  --output src/week05_node5_text_nav2_bridge/outputs/week05_text_to_nav2_results.csv
```

## Expected Evidence

The output CSV records:

- input instruction;
- expected and parsed landmark;
- parsed Nav2 goal coordinates;
- Nav2 action result;
- timeout status;
- feedback distance.

This is the minimal bridge needed before replacing the rule-based parser with a
VLM output parser.

## Result

The first online run completed:

```text
text parse: 8/8
text-to-nav2 execution: 8/8 succeeded
```

Evidence:

```text
src/week05_node5_text_nav2_bridge/outputs/week05_text_to_nav2_results.csv
```

This result only covers fixed landmark names in the TurtleBot3 map. It does not
test open-vocabulary language understanding or visual confirmation.
