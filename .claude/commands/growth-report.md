---
description: Run the agent chain (data-explorer, notebook-reviewer, model-builder, notebook-reviewer, ml-statistician, growth-strategy-partner, report-writer) on one project folder to produce a plain-language final report in Markdown and interactive HTML
argument-hint: <project-folder-name>
---

Produce a final growth report for the project folder `$ARGUMENTS` under `/Users/shrikar/Documents/Marketing Analytics` by orchestrating six subagents that exist in `.claude/agents/`, in this order: `data-explorer`, `notebook-reviewer` (on the exploration notebook), `model-builder`, `notebook-reviewer` (on the two modeling notebooks), `ml-statistician`, `growth-strategy-partner`, `report-writer`. You are the orchestrator only. Do not do their analysis and do not write the final report yourself; your context is full of briefs and hand-backs by the end, and the writer's must stay clean.

## Rules that keep the agents' context clean
- Brief each agent with **paths, not pasted text**. Never paste a report into a prompt; name the file and tell the agent to read it.
- Each brief is under 25 lines: PROJECT, what to read first, where to write, what the next agent will consume, and the one constraint that matters.
- Run the agents one at a time in the foreground. Do not run two at once; each depends on the previous one's files.
- After each agent returns, confirm its key output file exists and is non-empty before starting the next. If it is missing, stop and report.

## 0. Resolve the folder
- `$ARGUMENTS` may be the exact folder name, its two-digit prefix (`01`) or a distinctive word (`churn`). Match exactly one directory in the workspace root; otherwise list the candidates and stop.
- PROJECT is the absolute path. Confirm `problem_description.md` and `data/raw/` exist.
- Tell the user in one line which folder you resolved and that the agent chain will run in sequence, with a notebook review after each notebook stage.

## 1. data-explorer (foreground)
Brief: PROJECT; read `problem_description.md` first; do all exploration in `notebooks/01_exploration.ipynb`, executed; write everything under `reports/exploration/`; the model-builder will read `handoff_to_modeling.md` and `clean.parquet`; write for a non-technical reader. Confirm `reports/exploration/findings.md`, `data_dictionary.md`, `handoff_to_modeling.md` and `clean.parquet` exist, and that `notebooks/01_exploration.ipynb` exists and executed with zero error outputs (check with nbformat: no output of type `error` in any code cell).

## 1b. notebook-reviewer on the exploration notebook (foreground), then one fix round
Spawn `notebook-reviewer` with: PROJECT; the path `notebooks/01_exploration.ipynb`; companion files `reports/exploration/data_dictionary.md` and `reports/exploration/hypotheses.md`. If its verdict is FIX, send its numbered gap list verbatim to the data-explorer agent (SendMessage to its agent id) and wait for its reply; then re-run the reviewer once on the revised notebook. Record both reviewer reports in `PROJECT/reports/notebook_review.md` under "01_exploration". Proceed after the second review whatever its verdict, noting any remaining gaps in that file. Re-confirm the notebook has zero error outputs.

## 2. model-builder (foreground)
Brief: PROJECT; read `problem_description.md`, `reports/exploration/handoff_to_modeling.md` and `data_dictionary.md`; load `reports/exploration/clean.parquet`; do feature engineering in `notebooks/02_feature_engineering.ipynb` and modeling in `notebooks/03_modeling.ipynb`, both executed; write under `reports/modeling/`, `models/` and `src/`; tune with Optuna as its instructions say; the ml-statistician will read `model_card.md`, `tuning.md`, `scores.csv` and the tables. Confirm `reports/modeling/model_card.md`, `tuning.md`, `features.md`, `features.parquet` and `scores.csv` exist, and that `notebooks/02_feature_engineering.ipynb` and `notebooks/03_modeling.ipynb` exist and executed with zero error outputs.

## 2b. notebook-reviewer on the modeling notebooks (foreground), then one fix round
Spawn `notebook-reviewer` with: PROJECT; the paths `notebooks/02_feature_engineering.ipynb` and `notebooks/03_modeling.ipynb`; companion files `reports/modeling/features.md` and `reports/modeling/tuning.md`. If FIX, send the gap list verbatim to the model-builder agent and wait; re-run the reviewer once. Append both reports to `PROJECT/reports/notebook_review.md` under "02_feature_engineering and 03_modeling". Proceed after the second review, noting remaining gaps. Re-confirm both notebooks have zero error outputs.

## 3. ml-statistician (foreground)
Brief: PROJECT; read the exploration and modeling outputs as its instructions list; write `reports/ml_handoff_report.md`, `reports/tables/`, `reports/charts/` and the per-row score file; the growth-strategy-partner will read the handoff report from its file and may message follow-up questions. Record its agent id. Confirm `reports/ml_handoff_report.md` exists.

## 4. growth-strategy-partner (foreground)
Brief: PROJECT; read `problem_description.md` and `reports/ml_handoff_report.md` from disk (do not paste it); charts in `reports/charts/`; write `reports/executive_growth_strategy.md`; the ml-statistician's agent id for direct questions (SendMessage); two rounds maximum; if messaging fails, end with a `QUESTIONS FOR STATISTICIAN` block. Confirm the memo exists.

## 5. Dialogue log
Both agents message each other directly; the statistician appends new numbers to `reports/ml_followups.md`. After the partner returns, ask it with SendMessage for the verbatim questions it sent and, per question, the memo section affected and what changed. Write the reply, unedited, to `PROJECT/reports/agent_dialogue.md` under a "Round 1" heading (and further rounds if any). If the partner's message ends with a `QUESTIONS FOR STATISTICIAN` block, relay it yourself: SendMessage the questions to the statistician, then its answers to the partner, at most two rounds, and record every message verbatim in the same file. If there were no questions, write that in the file.

## 6. report-writer (foreground)
Spawn `report-writer` with a brief of under 15 lines: PROJECT; that all inputs are on disk under `reports/` (exploration, modeling, handoff report, strategy memo, followups, agent_dialogue) and it must read them itself; that it writes `reports/final_report.md` and `reports/final_report.html` and publishes the HTML with the Artifact tool; that it adds no analysis. Do not paste any report content, summary or finding into the brief. Confirm both files exist and the artifact link is in its reply.

## 7. Report back
Under 20 lines: the folder; one line per agent with its outcome and runtime, including both reviewer verdicts and the number of gaps fixed; the number of question rounds; the three findings exactly as the report-writer returned them; anything the consistency check flagged; the paths to `final_report.md` and `final_report.html`; the artifact link. Do not paste the reports into the chat and do not restate the findings in your own words.

Notes: never edit the agent definition files from this command; if an agent fails, report what it produced and stop rather than filling the gap yourself; never load the artifact-design or dataviz skills yourself, the report-writer does.
