# Week 2 Report: High-Value References and Research Path

## Goal

The goal of Week 2 was to understand the main references for
Vision-Language Navigation and decide which reproduction path is realistic for
this project.

## Work Completed

I organized the High-Value References into a practical reading and
implementation route. The main references are:

- R2R for the classic VLN benchmark and metrics.
- VLN-CE for continuous navigation closer to robot motion.
- Habitat-Lab / Habitat-Sim for embodied AI simulation.
- RxR for multilingual and richer route instructions.
- ROS 2 Nav2 for AMR navigation execution.

Supporting files:

- `src/week02_references/high_value_references.md`
- `src/week02_references/reference_matrix.csv`

## Key Finding

A full VLN model reproduction may be too large as the first baseline. A more
controlled and useful route is to treat the project as an integration problem:

> natural-language instruction -> structured waypoint or goal pose -> ROS 2
> Nav2-style navigation execution.

This keeps the project connected to VLN research while making the engineering
work testable in a ROS 2 AMR environment.

## Selected Baseline Direction

The selected baseline is a small language-to-waypoint interface. It will use a
limited landmark map and convert simple instructions into structured goal poses.
This baseline can later be connected to a Nav2 action interface.

## Metrics and Evidence Plan

For the language-to-waypoint baseline:

- instruction matching accuracy;
- number of supported landmarks;
- success and failure examples;
- generated goal pose format.

For the later AMR interface:

- whether the goal is accepted by Nav2;
- whether the robot reaches the goal;
- trajectory length;
- failure cases such as wrong landmark, wrong pose, collision, or planner
  failure.

## Next Step

Week 3 should implement the first minimal baseline and generate a small result
file that can be used in the report.
