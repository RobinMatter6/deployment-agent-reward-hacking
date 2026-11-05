# Dependency Fabrication in Repository Deployment Agents

This repository contains the code and data for the OpenCourse project at Uppsala University titled *Dependency Fabrication in Repository Deployment Agents*. The full report is available in [`Robin_Matter_OpenCourse_Dependency_Fabrication.pdf`](Robin_Matter_OpenCourse_Dependency_Fabrication.pdf). All section and table references below refer to this report.

Repository deployment agents such as Repo2Run and SetupX aim to set up repositories and are evaluated based on whether they can make the repositories' tests pass. I tested these agents on probe repositories with dependencies that were impossible to obtain. In most runs, the agents fabricated the missing dependency, creating a fake replacement to pass the tests. Their harnesses then mostly reported success.

Next, I tested rules intended to prevent this behavior (Section 6). I then built my own agent, MinimalSetupAgent, to test mitigations from the reward-hacking literature (Sections 8 and 9). Finally, I applied the most effective mitigation to Repo2Run and SetupX (Section 10). This reduced the number of runs with dependency fabrication from 16 out of 16 for MinimalSetupAgent and 15 out of 16 for both Repo2Run and SetupX to 0 out of 16 for all three agents on the probes used in the experiments.

## Repository structure

```text
Robin_Matter_OpenCourse_Dependency_Fabrication.pdf
                          The report (PDF)
agents/
  minimal_setup_agent/    MinimalSetupAgent and its interventions (Sections 8 and 9)
  repo2run/, setupx/      Harness versions used in Section 10,
                          with one folder per row of Table 5
probes/
  section6/               Probe repositories used in Section 6
  section8_10/            Probe repositories used in Sections 8–10
results/
  <experiment>.csv        One row per run, named after the report section and table
  runs/<experiment>/      Full run records, including conversations, commands,
                          and test results (grade/grade.json)
```