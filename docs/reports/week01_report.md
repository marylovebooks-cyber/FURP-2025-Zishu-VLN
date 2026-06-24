# Week 1 Report: Environment Setup and First Smoke Test

## Project Direction

The selected project direction is Vision-Language Navigation for an Autonomous
Mobile Robot. The long-term goal is to connect natural-language route
instructions with robot navigation behavior.

## Work Completed

I set up the FURP repository and started the initial robotics environment test.
The first technical direction was AMR integration using ROS 2 Humble and Nav2.
The initial setup was attempted on Windows 11 with WSL2 Ubuntu.

The Week 1 smoke test aimed to check whether a virtual mobile robot could be
loaded in a simulator and visualized through the ROS 2 toolchain.

Supporting file:

- `src/week01_environment/ros2_environment_notes.md`

## Result

The smoke test did not succeed. The virtual robot did not appear correctly in
the simulator. RViz2 also had graphics-related problems in WSL2. In addition,
local proxy/VPN behavior on Windows may have affected simulator and ROS 2
communication.

## Analysis

The main issue was environment stability rather than the navigation algorithm.
Gazebo, RViz2, ROS 2 middleware, and Nav2 require reliable graphics and local
network behavior. WSL2 is useful for command-line tools, but it is not ideal for
this full robotics simulation stack.

## Decision

The project should move to native Ubuntu 22.04 for later work. This gives a more
realistic ROS 2 development environment and reduces the risk that graphics or
network problems block the research.

## Next Step

Week 2 should focus on narrowing the research path through high-value
references, especially R2R, VLN-CE, Habitat-Lab, RxR, and ROS 2 Nav2.
