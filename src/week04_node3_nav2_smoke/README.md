# Week 4 / Node 3 Minimal Nav2 Smoke Test

## Purpose

This folder records a minimal version of ZhiruiSHEN-VLN Node 3:

> TurtleBot3 Gazebo simulation -> Nav2 bringup -> fixed goal pose -> robot movement.

This is not a VLN model yet. It records that the local Ubuntu 22.04 + ROS 2
Humble environment can run a Nav2-controlled TurtleBot3 robot in simulation.

## Environment

| Item | Value |
|---|---|
| OS | Ubuntu 22.04.5 LTS |
| ROS 2 | Humble |
| Robot | TurtleBot3 Burger |
| Simulator | Gazebo Classic 11 |
| Navigation stack | Nav2 |

## Important Fix

Gazebo initially failed because the online model database was disabled without
adding the local Gazebo model path. The robot spawned, but the world had no
`ground_plane`, so odometry showed the robot falling through the world.

Working Gazebo launch requires:

```bash
export GAZEBO_MODEL_DATABASE_URI=""
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

This avoids slow or failed online model downloads while still loading local
`ground_plane`, `sun`, and TurtleBot3 models.

## Commands

Start Gazebo:

```bash
export TURTLEBOT3_MODEL=burger
export GAZEBO_MODEL_DATABASE_URI=""
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/humble/share/turtlebot3_gazebo/models
export ROS_LOG_DIR=/home/mary/Documents/FURP-2025-Zishu-VLN/src/week04_node3_nav2_smoke/logs
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Start Nav2:

```bash
export TURTLEBOT3_MODEL=burger
export ROS_LOG_DIR=/home/mary/Documents/FURP-2025-Zishu-VLN/src/week04_node3_nav2_smoke/logs
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:=/opt/ros/humble/share/turtlebot3_navigation2/map/map.yaml
```

Send one fixed goal:

```bash
/usr/bin/python3 src/week04_node3_nav2_smoke/send_nav2_goal.py \
  --initial-x -2.0 \
  --initial-y -0.5 \
  --initial-yaw 0.0 \
  --goal-x 0.0 \
  --goal-y 0.0 \
  --goal-yaw 0.0 \
  --timeout-sec 180 \
  --output src/week04_node3_nav2_smoke/outputs/nav2_goal_result.csv
```

## Result

The final successful run produced:

```text
nav2_result = SUCCEEDED
duration_sec = 18.074
last_feedback_distance_m = 0.050
```

Evidence file:

```text
src/week04_node3_nav2_smoke/outputs/nav2_goal_result.csv
```

Final `/odom` sample after navigation:

```text
x = -0.2543
y = 0.2017
z = 0.0085
```

The goal was `(0.0, 0.0)`, so the robot moved from the spawn position near
`(-2.0, -0.5)` toward the target and Nav2 reported success.

## 10-Goal Benchmark

After the one-goal smoke test, the same Gazebo/Nav2 stack was extended to a
small automated benchmark:

```bash
/usr/bin/python3 src/week04_node3_nav2_smoke/run_10_goal_benchmark.py \
  --initial-x -2.0 \
  --initial-y -0.5 \
  --initial-yaw 0.0 \
  --timeout-sec 120 \
  --settle-sec 1.0 \
  --output src/week04_node3_nav2_smoke/outputs/nav2_10_goal_benchmark.csv
```

Result:

```text
10-goal benchmark complete: 10/10 succeeded
```

Evidence file:

```text
src/week04_node3_nav2_smoke/outputs/nav2_10_goal_benchmark.csv
```

This is a small fixed-goal navigation check: multiple Nav2 goals are sent
automatically and each goal is evaluated from the Nav2 action result.

## Screenshot Note

Desktop screenshot capture was attempted with `xwd`, but GNOME Wayland/XWayland
returned a `BadMatch` capture error. The reproducible evidence for this run is
therefore the CSV output plus ROS launch/topic logs.
