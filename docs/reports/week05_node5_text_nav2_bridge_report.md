# Week 5 Report: Minimal Text-to-Nav2 Bridge

## Goal

The goal for Week 5 is to connect the Week 3 language-to-waypoint idea with the
Week 4 Nav2 execution layer:

```text
text instruction -> coordinate parsing -> Nav2 goal -> robot movement
```

This is a minimal Node 5 bridge. It does not use Qwen or camera input yet.
The parser only handles the fixed landmark names and aliases listed in the
local `landmarks.json` file.

## Method

The bridge uses a small rule-based parser. Each instruction is matched to a
known landmark in:

```text
src/week05_node5_text_nav2_bridge/landmarks.json
```

The matched landmark provides:

```text
x, y, theta
```

Those values are converted into a `PoseStamped` in the `map` frame and sent to
Nav2 with `nav2_simple_commander.BasicNavigator`.

## Why This Step Matters

Week 3 only produced a waypoint-like JSON output. Week 4 showed that Nav2 can
execute fixed coordinates. Week 5 checks the connection between those two
layers in simulation.

The experiment is intentionally simple so that failures can be assigned to the
bridge or Nav2, rather than to VLM inference.

## Test Set

Input instructions:

```text
src/week05_node5_text_nav2_bridge/sample_text_nav2_instructions.csv
```

The eight target landmarks are selected from coordinates that were already
usable in the Week 4 TurtleBot3 10-goal run. This keeps the test focused on the
bridge wiring rather than on discovering new safe target points.

## Evidence Files

Script:

```text
src/week05_node5_text_nav2_bridge/text_to_nav2_goal.py
```

Online output:

```text
src/week05_node5_text_nav2_bridge/outputs/week05_text_to_nav2_results.csv
```

Dry-run output:

```text
src/week05_node5_text_nav2_bridge/outputs/week05_text_parse_dry_run.csv
```

## Result

Dry-run parsing result:

```text
text parse: 8/8
```

Online TurtleBot3 Gazebo + Nav2 result:

```text
text parse: 8/8
text-to-nav2 execution: 8/8 succeeded
```

CSV summary:

| Trial | Instruction | Parsed landmark | Nav2 result | Duration |
|---:|---|---|---|---:|
| 1 | go to center approach | center approach | SUCCEEDED | 1.809 s |
| 2 | move to the map center | map center | SUCCEEDED | 22.843 s |
| 3 | navigate to center lower | center lower | SUCCEEDED | 13.834 s |
| 4 | go to center upper left | center upper left | SUCCEEDED | 12.074 s |
| 5 | move to upper left | upper left | SUCCEEDED | 17.434 s |
| 6 | go to upper spawn side | upper spawn side | SUCCEEDED | 21.035 s |
| 7 | navigate to near spawn upper | near spawn upper | SUCCEEDED | 10.823 s |
| 8 | return to spawn | return spawn | SUCCEEDED | 10.221 s |

The longest run was the second instruction, `move to the map center`, at
22.843 seconds. All targets finished within the 120-second timeout.

## Current Scope

This is not an integrated VLN system yet. It is a fixed-landmark bridge:

```text
rule-based text parser -> fixed map coordinates -> Nav2
```

The next step is to replace or augment the rule-based parser with VLM output,
then run a small integrated evaluation with visual confirmation.

The result should therefore be described as a minimal text-to-Nav2 execution
check, not as open-vocabulary language navigation.
