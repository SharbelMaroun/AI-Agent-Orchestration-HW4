# Comprehensive Document Translation & Summary Report

**Source Document:** ex04-gaphify-obcidian-Reverse-engineering.pdf (10 pages)

---

--- PAGE 1 ANALYSIS ---

This document is the cover page for an academic or technical assignment.

**Header Information:**
* Assignment 04

**Main Title (Bilingual):**
* The Hebrew text translates to: "Reverse Engineering, Debugging, and Artificial Intelligence, Token-Efficient Agentic via Grphify and Obsidian-1"
* The English text provided is: "EX04 - Reverse Engineering, Debugging and Token-Efficient Agentic AI with Grphify and Obsidian"

**Metadata:**
* Assignment: 04
* Lesson: L07

**Author and Copyright:**
* Author: Dr. Yoram Segal
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

**Publication Details:**
* Date: June 2026
* Version: 1.0

--- PAGE 2 ANALYSIS ---

**Keywords Section**
The page begins with a list of keywords, presented in a mix of English and Hebrew. Following the strict translation rules, the English terms are:
Token, Debugging, Reverse Engineering, Obsidian, Grphify, Code Visualization, LangGraph, CrewAI, Agentic AI, Efficiency, Context, Lost in the Middle, God Nodes, Knowledge Graph, Block Schema, OOP, graph.json, hot.md, index.md, Window Architecture, Knowledge-Based Navigation, BugsInPy.

**Table of Contents**
The document provides a structured table of contents. The following table represents the content, with Hebrew labels translated to English:

| Section Number | Section Title | Page Number |
| :--- | :--- | :--- |
| 1 | Assignment Overview | 3 |
| 2 | Base Repositories | 3 |
| 3 | Objectives | 4 |
| 4 | Research Questions | 4 |
| 5 | Core Tasks | 5 |
| 5.1 | Building Grphify and Documentation | 5 |
| 5.2 | Reverse Engineering Unfamiliar Code | 5 |
| 5.3 | Debugging via Agentic AI | 5 |
| 5.4 | Code Repair and Improvement | 6 |
| 5.5 | Proof of Token Efficiency | 6 |
| 5.6 | Extensions and Original Initiatives | 6 |
| 6 | Planning & Efficiency | 7 |
| 6.1 | Do | 7 |
| 6.2 | Don't | 8 |
| 7 | Deliverables | 8 |
| 8 | README Requirements | 9 |
| 9 | Recommended Repository Structure | 10 |
| 10 | Expectations | 10 |

**Footer**
* Page Number: 2
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 3 ANALYSIS ---

**1 Assignment Overview**

In this assignment, you are required to investigate an unfamiliar Python codebase, analyze it using Grphify, represent the knowledge within Obsidian, and deploy an AI agent based on LangGraph or CrewAI for analysis, debugging, and explanation of bugs. The goal of the work is to demonstrate how to represent code as a graph, document hierarchy, and navigate knowledge to understand complex systems, perform reverse engineering, and save tokens compared to naive code reading.

The work is based on key principles from the lecture: the "Lost in the Middle" problem, context window decay, and the use of index.md and hot.md for central navigation, and converting a codebase into a graph space that can be investigated systematically. Accordingly, you are not required to just fix a bug, but to build a complete engineering investigation process, document it, and present clear proof of graph-oriented work over code-focused reading.

The work will be performed in pairs and will involve a full Python project from GitHub. The submission must present the structure of the unfamiliar code, debugging capability, extraction of insights from reverse engineering, architectural documentation, and the use of AI agents.

**2 Base Repositories**

You must choose one base repository for the work, and integrate between several repositories if necessary:

* soarsmu/BugsInPy — A repository of real bugs in real Python projects, and therefore especially suitable for groups that want a more realistic research scenario.
* martinpeck/broken-python — A collection of broken Python code snippets intended for debugging and code improvement exercises.
* andela/buggy-python — A repository of several scripts intended to test the ability to identify and fix problems in code.

The chosen repository must appear in the README, along with a short explanation of why it was chosen and how it fits the goals of the assignment.

**Footer**
* Page Number: 3
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 4 ANALYSIS ---

**3 Objectives**

The assignment requires demonstrating the ability to perform a systematic investigation of an unfamiliar system. You must build a graphical representation of the codebase, understand the actual architecture, formulate research and understanding questions, deploy an AI agent in an efficient and controlled manner to locate a bug, fix it, and present the change both at the code level and at the knowledge and documentation level.

It is required not only to show what was fixed, but also how you arrived at the fix, which components were central, what connections between entities assisted you, and what was the value of Grphify and Obsidian throughout the process.

**4 Research Questions**

During the assignment, you must explicitly address the following questions:

* What is the actual architecture of the project, and what did you discover about it that was not clear at first glance?
* Which components, modules, classes, or functions are the most central in the system?
* Where are the complex focal points, responsibilities, or "God Nodes" located?
* How can the code be extracted from block schemas and OOP structures even when the original documentation is missing or partial?
* How did you identify the bug, what was the root cause, and which steps led you to it?
* What was the advantage of the graphical representation and navigation via Obsidian compared to linear reading of files?
* How did the use of an AI agent in a graph-oriented approach save tokens or reduce redundant code readings?
* What improvements, extensions, or additional agent mechanisms did you add along the way?

These questions are part of the assignment itself and must be expressed in the README, in the reports, and in the Obsidian files.

**Footer**
* Page Number: 4
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 5 ANALYSIS ---

**5 Core Tasks**

**5.1 Building Grphify Representation and Obsidian Documentation**

You must generate a graph representation of the codebase using Grphify and build an Obsidian vault that organizes the project as an active knowledge space rather than just a collection of files.

It is required to include at least:
* **index.md** — A central entry page describing the system structure and primary navigation paths.
* **hot.md** — A page focused on the critical area for bug investigation.
* Additional Markdown pages documenting central components, tests, research findings, suspects, and the repair process.

**5.2 Reverse Engineering of Unfamiliar Code**

You must perform reverse engineering on the chosen codebase. You are required to extract insights from the code and present at least two central diagrams:
* A block architecture diagram describing the primary parts of the system and the flow between them.
* An OOP diagram describing classes, usage relationships, composition, inheritance, encapsulation, or relevant design patterns.

Do not settle for a directory structure or a file list. The diagrams must reflect an engineering understanding of the code.

**5.3 Debugging via AI Agent**

You must build and deploy an AI agent using LangGraph or CrewAI for the purpose of investigation, localization, and explanation of the bug. The agent must operate using a graph-oriented approach: it must first rely on Grphify outputs and Obsidian pages, and only afterwards request relevant code snippets.

You must explain how the agent workflow is built, what the function of each step is, and what mechanisms were implemented to reduce context to maintain efficiency.

**Footer**
* Page Number: 5
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 6 ANALYSIS ---

**5.4 Code Repair and Improvement**

After locating the bug, you must perform an actual code repair. You must clearly present what the problem was, why it occurred, what change was made, and how the success of the repair was verified.

You are also required to present a "before and after" snapshot at the knowledge level: which pages, nodes, links, or additional insights were added to Obsidian following the investigation and repair, and how your understanding of the architecture has changed.

**5.5 Proof of Token Savings**

You must perform a comparison between two work states:
- A naive state, where the agent or workflow operates on raw files without sufficient focus.
- A graph-guided state, where the agent operates via Grphify, index.md, and Obsidian hot.md pages.

You must present a clear comparison between the states, including at least:
- Number of tokens consumed.
- Number of files or text units read.
- Number of iterations or investigation cycles.
- Quality or speed of reaching the root cause and the repair.

**5.6 Extensions and Original Initiatives**

The assignment is a baseline only. As part of the work, you are required to propose at least one original extension, additional analysis, or improvement beyond the minimum requirements.

Possible examples:
- Ranking nodes by proximity or centrality for failed tests.
- Dynamic creation of hot.md from git diff and graph.json.
- Identification of orphaned components and automatic documentation generation for them.
- Identification of overloaded connections or responsibilities and refactoring suggestions.

**Footer**
* Page Number: 6
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 7 ANALYSIS ---

- Comparison of architecture before and after repair using graphs or summaries.
- Generation of a report on the impact: what changed in the class or function.

**6 Planning & Efficiency**

The goal of this section is to help you complete the task within a reasonable time, even if you are working with free accounts and LLM reading limits. The most important principle is to minimize scope, work in stages, and activate the AI only once you have established an organized context.

**6.1 Do:**

- Choose one small or medium bug, not a whole system.
- Start with local Grphify and create graph.json, index.md, and hot.md.
- Use Obsidian to build a short work map: what is the problem, what are the suspects, what was checked, and what was fixed.
- Activate the AI only after you have an organized context.
- Prefer LangGraph if you are working with a limited free account, as it is easier to control the number of reads and steps.
- Measure along the way how many files you read, how many LLM reads there were, and how many tokens were consumed.
- If you chose BugsInPy, work in an isolated environment, and preferably Docker, so as not to waste time on dependency issues.

**Footer**
- Page Number: 7
- Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 8 ANALYSIS ---

**6.2 Don't:**

* Do not choose too many bugs or a project that is too large.
* Do not send all the code to the LLM at once.
* Do not build a workflow with too many agents and too many dependencies.
* Do not start with BugsInPy if you do not have basic experience with Python and environments/dependencies.
* Do not turn the assignment into a complete project. A small, well-explained case with a clear before/after is preferable.
* Do not skip documentation. Without a README, Obsidian, diagrams, and screenshots, it is impossible to prove the process.

**7 Deliverables:**

The submission must be a full GitHub repository, including at least:

* Full Python code of the solution.
* Implementation of an agent workflow in LangGraph or CrewAI.
* Grphify outputs, such as GRAPH_REPORT.md, graph.json, or parallel outputs.
* A full Obsidian vault with linked Markdown pages, including index.md and hot.md.
* A bug analysis report, including a description of the problem, the root cause, the investigation process, and the repair.
* A token comparison report between the baseline and the graph-guided approach.
* Block architecture diagram.
* OOP diagram.
* Proof of before/after code repair and system understanding.
* Documentation of extensions and original ideas of the group.

**Footer**
* Page Number: 8
* Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 9 ANALYSIS ---

**8 Detailed README Requirements**

The README.md file is a substantial part of the submission. It must be rich, clear, and readable for an external reader. The README must include:

- Description of the selected repository and justification for the choice.
- Description of the problem or bug investigated.
- Research questions and the understanding that guided the work.
- Overview of the architecture as extracted from the code.
- Description of the agent workflow built.
- Explanation of how Grphify and Obsidian were used.
- Explanation of the reverse engineering process performed.
- Description of the bug, the root cause, and the fix.
- Comparison of before and after.
- Comparison of token efficiency.
- Details of extensions and original ideas of the group.
- Clear running instructions.

In addition, the README must include visual elements such as screenshots, graphs, block diagrams, OOP diagrams, flowcharts, or any other visual illustration that supports the analysis and presentation of the process.

**Footer**
- Page Number: 9
- Copyright Notice: All rights reserved to Dr. Yoram Segal (C)

--- PAGE 10 ANALYSIS ---

**9 Recommended Repository Structure**

The suggested structure for the submission repository is as follows:

* README.md
* requirements.txt
* pyproject.toml
* src/
* tests/
* obsidian/
* reports/
* artifacts/
* data/

The structure can be adapted to the needs of the project, but it must remain consistent, clear, and easy to navigate.

**10 Expectations**

The expected work is a full engineering project, demonstrating construction, initiative, and the ability to generate meaningful insights from existing code. You are required to demonstrate debugging capabilities in unfamiliar code, extraction of insights through reverse engineering, production of summaries at the architecture and OOP levels, real code improvement, and proof of the state before and after using an Obsidian-based approach.

This assignment is not intended for mechanical execution of technical steps alone. It is intended to examine how you investigate a system, how you document it, how you operate an AI agent as an engineering tool, and how you prove that graph-based work and focused context are more efficient than raw code reading.

***

**Footer**
* All rights reserved to Dr. Yoram Segal (C)
* Page Number: 10

---

## Cross-Reference Clarifications

- **Page 2 → Page 3:** The Table of Contents lists Section 1 (Assignment Overview) and Section 2 (Base Repositories) as being located on page 3.
- **Page 2 → Page 4:** The Table of Contents lists Section 3 (Objectives) and Section 4 (Research Questions) as being located on page 4.
- **Page 2 → Page 5:** The Table of Contents lists Section 5 (Core Tasks) and subsections 5.1 through 5.3 as being located on page 5.
- **Page 2 → Page 6:** The Table of Contents lists subsections 5.4 through 5.6 as being located on page 6.
- **Page 2 → Page 7:** The Table of Contents lists Section 6 (Planning & Efficiency) and subsection 6.1 as being located on page 7.
- **Page 2 → Page 8:** The Table of Contents lists subsection 6.2 and Section 7 (Deliverables) as being located on page 8.
- **Page 2 → Page 9:** The Table of Contents lists Section 8 (README Requirements) as being located on page 9.
- **Page 2 → Page 10:** The Table of Contents lists Section 9 (Recommended Repository Structure) and Section 10 (Expectations) as being located on page 10.
- **Page 3 → Page 5:** The assignment requires the use of Grphify and Obsidian, which are detailed in the core tasks on page 5.
- **Page 7 → Page 5:** The planning section references the creation of graph.json, index.md, and hot.md, which are defined as core tasks on page 5.
- **Page 8 → Page 5:** The deliverables list requires Grphify outputs and an Obsidian vault, which are defined as core tasks on page 5.
