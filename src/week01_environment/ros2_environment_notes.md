# Week 1 Environment Notes

## Goal

Set up an initial ROS 2 navigation environment and run a smoke test for the
Vision-Language Navigation for AMR project.

## Initial Environment

| Item | Record |
|---|---|
| OS | Windows 11 with WSL2 Ubuntu |
| Robotics stack | ROS 2 Humble, Nav2 attempt |
| Simulator/display tools | Gazebo and RViz2 |
| Project direction | Vision-Language Navigation / AMR integration |

## Smoke Test Attempt

The first smoke test attempted to start a ROS 2 navigation simulation and check
whether a virtual mobile robot could be loaded and visualized.

Expected result:

- Gazebo loads the simulation world.
- The robot model appears in the scene.
- RViz2 can visualize robot state, map, and navigation information.
- ROS 2 nodes communicate normally between simulator and navigation stack.

Actual result:

- The virtual robot did not appear correctly in the simulator.
- RViz2 crashed or became unusable because of WSL2 graphics limitations.
- Simulator and ROS 2 communication appeared unstable.
- Local proxy/VPN behavior on Windows likely interfered with local ROS 2 or
  simulator traffic.

## Diagnosis

The failure was treated as an environment issue rather than a navigation
algorithm issue. WSL2 is convenient for command-line development, but a Gazebo +
RViz2 + ROS 2 navigation stack depends on graphics, networking, and middleware
communication. These parts are fragile in WSL2.

## Decision

Move the project to native Ubuntu 22.04 for later weeks. This should reduce
graphics and networking problems and make ROS 2/Nav2 experiments more reliable.

## Evidence to Keep

- ROS 2 install commands.
- Terminal output from failed simulator launches.
- Screenshots or logs of RViz2/Gazebo failures if available.
- Notes on proxy/VPN state during the test.
