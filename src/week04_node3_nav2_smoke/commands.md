# Week 4 Node 3 Command Log

## Package Verification

```bash
ros2 pkg list | grep nav2_bringup
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep gazebo_ros
```

Observed packages:

```text
nav2_bringup
turtlebot3_gazebo
gazebo_ros
gazebo_ros_pkgs
```

## Failed Attempt 1: Default TurtleBot3 Gazebo Launch

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Problem:

```text
Service /spawn_entity unavailable. Was Gazebo started with GazeboRosFactory?
```

Reason:

Gazebo was trying to access the online model database and did not finish
bringing up the factory service in time.

## Failed Attempt 2: Disable Online Model Database Only

```bash
export TURTLEBOT3_MODEL=burger
export GAZEBO_MODEL_DATABASE_URI=""
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Problem:

```text
Unable to find uri[model://ground_plane]
Unable to find uri[model://sun]
```

Symptom:

```text
/odom z became a huge negative value
```

Reason:

The online model database was disabled, but Gazebo was not given the local model
path for `ground_plane` and `sun`.

## Successful Gazebo Launch

```bash
export TURTLEBOT3_MODEL=burger
export GAZEBO_MODEL_DATABASE_URI=""
export GAZEBO_MODEL_PATH=/usr/share/gazebo-11/models:/opt/ros/humble/share/turtlebot3_gazebo/models
export ROS_LOG_DIR=/home/mary/Documents/FURP-2025-Zishu-VLN/src/week04_node3_nav2_smoke/logs
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Validation:

```bash
ros2 topic list | sort | grep -E '^/(cmd_vel|odom|scan|tf|clock|joint_states)$'
ros2 topic echo /odom --once
```

Observed:

```text
/clock
/cmd_vel
/joint_states
/odom
/scan
/tf
```

The corrected `/odom` z value was approximately:

```text
z = 0.0085
```

## Successful Nav2 Launch

```bash
export TURTLEBOT3_MODEL=burger
export ROS_LOG_DIR=/home/mary/Documents/FURP-2025-Zishu-VLN/src/week04_node3_nav2_smoke/logs
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:=/opt/ros/humble/share/turtlebot3_navigation2/map/map.yaml
```

Reason for `use_sim_time:=True`:

Gazebo publishes `/clock`. Nav2, RViz, TF, AMCL, and the simulated robot must
use the same simulation time source.

## Successful Fixed Goal

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

Result:

```text
nav2_result = SUCCEEDED
duration_sec = 18.074
last_feedback_distance_m = 0.050
```

## Successful 10-Goal Benchmark

```bash
/usr/bin/python3 src/week04_node3_nav2_smoke/run_10_goal_benchmark.py \
  --initial-x -2.0 \
  --initial-y -0.5 \
  --initial-yaw 0.0 \
  --timeout-sec 120 \
  --settle-sec 1.0 \
  --output src/week04_node3_nav2_smoke/outputs/nav2_10_goal_benchmark.csv
```

Terminal output:

```text
Nav2 is ready for use!
Navigating to goal: -1.5 -0.5...
Navigating to goal: -1.0 -0.5...
Navigating to goal: -0.5 -0.5...
Navigating to goal: 0.0 -0.5...
Navigating to goal: 0.0 0.0...
Navigating to goal: -0.5 0.0...
Navigating to goal: -1.0 0.0...
Navigating to goal: -1.5 0.0...
Navigating to goal: -2.0 0.0...
Navigating to goal: -2.0 -0.5...
10-goal benchmark complete: 10/10 succeeded
results: src/week04_node3_nav2_smoke/outputs/nav2_10_goal_benchmark.csv
```

CSV summary:

```text
1 center_approach     SUCCEEDED 1.806 s
2 left_to_center_line SUCCEEDED 3.011 s
3 near_center_left    SUCCEEDED 2.464 s
4 center_lower        SUCCEEDED 3.011 s
5 map_center          SUCCEEDED 9.674 s
6 center_upper_left   SUCCEEDED 11.425 s
7 upper_left          SUCCEEDED 11.494 s
8 upper_spawn_side    SUCCEEDED 66.122 s
9 near_spawn_upper    SUCCEEDED 10.263 s
10 return_spawn       SUCCEEDED 9.020 s
```

## Screenshot Attempt

```bash
xwd -root -silent -out src/week04_node3_nav2_smoke/outputs/nav2_smoke_desktop.xwd
```

Result:

```text
X Error of failed request: BadMatch (invalid parameter attributes)
```

Reason:

The desktop session appears to restrict root-window capture, likely because of
GNOME Wayland/XWayland behavior. The retained evidence is the result CSV and
ROS launch logs.
