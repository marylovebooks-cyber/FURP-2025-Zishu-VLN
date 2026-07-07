# Week 4 Report: Node 3 10-Goal Nav2 Benchmark

## Goal

The goal was to extend the minimal Node 3 Nav2 smoke test from one fixed goal
to an automated 10-goal navigation run in the standard TurtleBot3 simulation
map. This is intended as a small local check of the Nav2 execution layer, not
as a full VLN benchmark.

## Why This Step Matters

The one-goal smoke test showed that TurtleBot3, Gazebo, AMCL, and Nav2 could
work together on this machine. Running 10 goals adds a simple repeatability
check: the robot has to accept new goals, plan paths, execute motion, and
return a Nav2 action result without manual RViz clicking.

This is still not VLN. It only checks the navigation execution layer that will
be needed before connecting language-derived waypoints to the robot.

## Environment

The benchmark used the same confirmed stack as the smoke test:

- Ubuntu 22.04.5 LTS.
- ROS 2 Humble.
- TurtleBot3 Burger.
- Gazebo Classic 11.
- Nav2 with TurtleBot3's standard map.

Gazebo was launched with local model paths to avoid online model database
failures:

```bash
export GAZEBO_MODEL_DATABASE_URI=""
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

## Navigation Script

Script:

```text
src/week04_node3_nav2_smoke/run_10_goal_benchmark.py
```

The script uses `nav2_simple_commander.BasicNavigator` to:

- publish the initial pose in the `map` frame;
- wait until Nav2 is active;
- send 10 fixed `PoseStamped` goals;
- record duration, Nav2 result, timeout status, and feedback distance;
- save the run as a CSV evidence file.

Command:

```bash
/usr/bin/python3 src/week04_node3_nav2_smoke/run_10_goal_benchmark.py \
  --initial-x -2.0 \
  --initial-y -0.5 \
  --initial-yaw 0.0 \
  --timeout-sec 120 \
  --settle-sec 1.0 \
  --output src/week04_node3_nav2_smoke/outputs/nav2_10_goal_benchmark.csv
```

## Result

The run completed successfully:

```text
10-goal benchmark complete: 10/10 succeeded
```

Evidence:

```text
src/week04_node3_nav2_smoke/outputs/nav2_10_goal_benchmark.csv
```

CSV summary:

| Trial | Label | Goal `(x, y)` | Result | Duration |
|---:|---|---:|---|---:|
| 1 | center_approach | `(-1.50, -0.50)` | SUCCEEDED | 1.806 s |
| 2 | left_to_center_line | `(-1.00, -0.50)` | SUCCEEDED | 3.011 s |
| 3 | near_center_left | `(-0.50, -0.50)` | SUCCEEDED | 2.464 s |
| 4 | center_lower | `(0.00, -0.50)` | SUCCEEDED | 3.011 s |
| 5 | map_center | `(0.00, 0.00)` | SUCCEEDED | 9.674 s |
| 6 | center_upper_left | `(-0.50, 0.00)` | SUCCEEDED | 11.425 s |
| 7 | upper_left | `(-1.00, 0.00)` | SUCCEEDED | 11.494 s |
| 8 | upper_spawn_side | `(-1.50, 0.00)` | SUCCEEDED | 66.122 s |
| 9 | near_spawn_upper | `(-2.00, 0.00)` | SUCCEEDED | 10.263 s |
| 10 | return_spawn | `(-2.00, -0.50)` | SUCCEEDED | 9.020 s |

The eighth goal took the longest. From the logs and timing, this likely means
Nav2 spent more time planning or adjusting around the map geometry. It still
finished within the 120-second timeout and returned `SUCCEEDED`.

## Current Status Compared With ZhiruiSHEN-VLN

This reaches a comparable minimal Node 3 checkpoint: an automated multi-goal
Nav2 run in simulation with a recorded 10/10 success result.

The remaining difference is scope. Zhirui's repository continues beyond this
into richer pipeline nodes. This repository currently has a smaller, fixed-goal
Nav2 navigation check that can later be connected to the Week 3
language-to-waypoint script.
