# Week 4 Report: Minimal Node 3 Nav2 Smoke Test

## Goal

The goal was to reproduce a small part of ZhiruiSHEN-VLN Node 3: run a
simulated mobile robot, start Nav2, send one fixed goal pose, and confirm that
the robot moves under Nav2 control.

## Why This Step Matters

The previous Week 3 baseline only converted language into a toy waypoint. It did
not prove that a robot could execute a navigation goal. This Week 4 smoke test
checks the missing AMR execution layer:

```text
fixed goal pose -> Nav2 -> TurtleBot3 Gazebo movement
```

Once this works, the Week 3 language-to-waypoint output can be connected to
Nav2 in a later step.

## Environment Confirmation

Confirmed:

- Ubuntu 22.04.5 LTS.
- ROS 2 Humble.
- `ros2` CLI available.
- Nav2 packages installed.
- TurtleBot3 Gazebo packages installed.
- Gazebo ROS packages installed.

Key package checks:

```text
nav2_bringup
turtlebot3_gazebo
gazebo_ros
gazebo_ros_pkgs
```

## Simulation Setup

The selected smoke-test stack was TurtleBot3 Burger in Gazebo Classic with
TurtleBot3's standard Nav2 launch files. This was chosen because it is a
standard ROS 2/Nav2 tutorial stack and is much more reproducible than building a
custom robot model for the first test.

## Issue Found and Fixed

Gazebo first failed to spawn the robot because `/spawn_entity` was unavailable.
The root cause was Gazebo trying to access the online model database. After
disabling the online model database, a second issue appeared: the world could
not find `ground_plane` and `sun`, so the robot fell through the world.

The fix was to disable the online model database while explicitly adding local
Gazebo models:

```bash
export GAZEBO_MODEL_DATABASE_URI=""
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/humble/share/turtlebot3_gazebo/models
```

After this, TurtleBot3 spawned successfully and `/odom`, `/scan`, and `/cmd_vel`
were available.

## Nav2 Goal Test

The test used a scripted goal sender:

```text
src/week04_node3_nav2_smoke/send_nav2_goal.py
```

Initial pose:

```text
x = -2.0, y = -0.5, yaw = 0.0
```

Goal pose:

```text
x = 0.0, y = 0.0, yaw = 0.0
```

## Result

The final successful run returned:

```text
nav2_result = SUCCEEDED
duration_sec = 18.074
last_feedback_distance_m = 0.050
```

Evidence:

```text
src/week04_node3_nav2_smoke/outputs/nav2_goal_result.csv
```

Final `/odom` sample:

```text
x = -0.2543
y = 0.2017
z = 0.0085
```

This records one successful fixed-goal Nav2 run. The robot moved from the spawn
area toward the target, and Nav2 returned `SUCCEEDED`.

## Current Status Compared With ZhiruiSHEN-VLN

This reaches the first part of a minimal Node 3 reproduction: basic simulated
Nav2 navigation works for one fixed goal.

The follow-up 10-goal run is recorded separately in:

```text
docs/reports/week04_node3_10_goal_benchmark_report.md
```
