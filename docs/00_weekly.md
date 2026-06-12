# Weekly Progress Log

> Update this file **every week**. Add a new entry at the top for each week.
> This is the first thing we check during review. Keep it honest and specific — it also feeds your attendance record (Rule 1).

**How to use:** copy the *Week template* block below for each new week. Newest week goes at the top.

---

## Week template — copy me

### Week N — YYYY-MM-DD

**Attended this week's meeting:** Yes / No (if No, did you email leave? Yes / No)

**Progress this week**
- _What did you actually do / finish?_

**Challenges & blockers**
- _What got in the way? What are you stuck on?_

**Next steps**
- _What will you do next week?_

**Hours spent (optional):** _e.g. 6h_

**Links (optional):** _commits, notebooks, docs, datasets..._

---

<!-- =================  YOUR ENTRIES BELOW  ================= -->

### Week 1 — 2026-06-12

**Attended this week's meeting:** Yes 

**Progress this week**
- Set up repository from the FURP template.
- [cite_start]Chose the **AMR Integration** track[cite: 14].
- [cite_start]Attempted the Week 1 smoke test [cite: 29] by installing ROS 2 Humble and Nav2 on Windows 11 (WSL2 Ubuntu).

**Challenges & blockers**
- **Smoke test failed:** The virtual robot did not appear in the simulator.
- **Issue 1 (Graphics Crash):** The default Windows WSL2 graphics driver is incompatible with the RViz2 display tool, causing it to crash immediately.
- **Issue 2 (Network Timeout):** My Windows proxy/VPN intercepted the local network traffic. This prevented the 3D simulator (Gazebo) from communicating with ROS 2, causing it to time out before the robot could load.
- I tried to bypass the 3D interface to fix the crashes, but the system still failed to spawn the robot.

**Next steps**
- Ask the teaching team if there is a known fix for WSL2 + ROS 2 proxy and graphics conflicts.
- [cite_start]If AMR integration is too unstable on WSL2, I will switch to the **Habitat RL navigation path** [cite: 31] for Week 2. Habitat runs in the background without a 3D user interface, which should completely avoid these WSL2 bugs.
- _..._

**Hours spent (optional):**

**Links (optional):**
