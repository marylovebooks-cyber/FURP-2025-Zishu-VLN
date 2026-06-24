# Week 2 High-Value References

## Purpose

The goal of Week 2 was to narrow the project from a broad VLN topic into a
reproducible AMR-oriented research path. The selected direction is:

> Natural-language instruction -> structured waypoint or goal pose -> ROS 2
> Nav2-style navigation execution.

This is smaller than a full end-to-end VLN system, but it is appropriate for a
FURP project because it can produce runnable evidence, metrics, and a clear
integration demo.

## Reading Priority

| Priority | Reference | Why it matters for this project |
|---|---|---|
| 1 | R2R: Vision-and-Language Navigation in Real Environments | Defines the classic VLN task and metrics such as SR, SPL, and navigation error. |
| 2 | VLN-CE: Vision-and-Language Navigation in Continuous Environments | Moves VLN from graph-based viewpoints toward continuous robot-like motion. |
| 3 | Habitat-Lab / Habitat-Sim | Provides embodied AI simulation tools used by many navigation baselines. |
| 4 | RxR: Room-Across-Room | Useful for multilingual and richer route instructions, but too large for the first baseline. |
| 5 | ROS 2 Nav2 | Provides the AMR-side navigation stack for executing goal poses and waypoints. |

## Key Takeaways

### R2R

R2R is the starting point for understanding VLN. The agent receives a natural
language route instruction and must navigate through indoor visual observations.
The most important contribution for this project is not the exact model, but the
evaluation style: success rate, path length, SPL, and final distance to goal.

Project use:

- Defines what "following an instruction" means.
- Provides metric vocabulary for reports.
- Helps separate language grounding errors from navigation execution errors.

### VLN-CE

VLN-CE is closer to robotics because it studies navigation in continuous
environments. Instead of only choosing the next graph node, the agent must deal
with more realistic movement. This is more relevant to AMR integration.

Project use:

- Supports the decision to connect VLN output to robot-executable goals.
- Motivates using ROS 2/Nav2 for the low-level navigation part.
- Gives a bridge between benchmark VLN and AMR execution.

### Habitat-Lab

Habitat-Lab is a practical simulation platform for PointNav, ObjectNav, and
continuous navigation tasks. It is useful if the project later needs a simulator
baseline before testing with ROS 2.

Project use:

- Candidate simulation baseline if Nav2/Gazebo is unstable.
- Useful for comparing navigation metrics and failure cases.
- Good fallback for non-ROS experiments.

### RxR

RxR extends route instruction following with richer and multilingual language.
It is valuable for background reading but should not be the first reproduction
target because the data and models are larger.

Project use:

- Possible later extension for multilingual instruction analysis.
- Helps justify why this project starts with a smaller command set.

### ROS 2 Nav2

Nav2 is the most important AMR integration reference. It converts a map, robot
state, costmaps, planners, controllers, and goal poses into navigation behavior.
For this project, the VLN side can output a target pose, and Nav2 can execute it.

Project use:

- Week 3/4 baseline target: send a structured goal pose.
- Final integration target: language instruction becomes a robot navigation
  command.
- Provides concrete evidence through trajectories, logs, maps, and screenshots.

## Selected Baseline Direction

The first baseline should not attempt full VLN model training. The selected
baseline is a controlled language-to-goal interface:

1. Define a small indoor map with named landmarks.
2. Map simple English instructions to goal poses.
3. Export the goal in a ROS 2/Nav2-compatible structure.
4. In Week 4, send the goal to a simulator or Nav2 action interface.

This creates a testable integration path while leaving room for a later
improvement, such as better instruction parsing, landmark grounding, or route
decomposition.
