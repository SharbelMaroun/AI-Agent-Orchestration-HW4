# Comprehensive Document Translation & Summary Report

**Source Document:** L07-Lesson-Summary.pdf (15 pages)

---

--- PAGE 1 ANALYSIS ---

This document is the title page for a lecture series.

**Header Information:**
* Lecture 07

**Main Title:**
* Reverse Engineering of Graph Knowledge Systems with Grphify and Obsidian

**Subtitle/Metadata:**
* Lecture 07 | Lecture Summary

**Author/Copyright Information:**
* Dr. Yoram Segal
* All rights reserved to Dr. Yoram Segal (c)

**Date and Versioning:**
* June 2026
* Version 1.0

**Footer Information:**
* Study Document - Recorded Lecture Summary

--- PAGE 2 ANALYSIS ---

**Keywords Section**
The page begins with a list of keywords, presented as a mix of English terms and their Hebrew equivalents. The English terms are: Reverse Engineering, Obsidian, Grphify, Centrality, Knowledge Graph, Single Point of Failure, Bridges, Hubs, Community Detection, Context Window, Token Efficiency, RAG, Compaction, Lost in the Middle, Vault, graph.json, hot.md, index.md, Ambiguous, Inferred, Extracted, Confusion, BugsInPy, AI, LangGraph, CrewAI, Matrix.

**Table of Contents**
The document provides a table of contents with page numbers. The entries are presented in a bilingual format (Hebrew followed by English). The English translations are as follows:

| Section Number | Section Title | Page |
| :--- | :--- | :--- |
| 1 | Introduction | 4 |
| 2 | The Context Window Bottleneck | 4 |
| 2.1 | RAG: The Three-Layer Architecture | 4 |
| 3 | Grphify vs. Obsidian | 5 |
| 4 | Grphify Strength: Almost Free Analysis | 6 |
| 4.1 | Obsidian Strength: The Wikipedia of the Project | 6 |
| 4.2 | Core Concepts | 6 |
| 5 | The Three Edge Types | 7 |
| 6 | Token Efficiency | 8 |
| 7 | The Graph Solution: Targeted Retrieval | 8 |
| 7.1 | Centrality and Communities | 9 |
| 8 | What the Community Teaches Us About Architecture | 9 |
| 8.1 | The "Lost in the Middle" Problem and Compaction | 10 |
| 9 | Reading the Graph | 10 |
| 10 | Advantages and Disadvantages | 11 |
| 10.1 | Matching the PRD for Implementation | 11 |
| 10.2 | The Assignment (EX04): Reverse Engineering with AI Agents | 11 |
| 11 | | 12 |

**Footer Information**
* Page number: 2
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 3 ANALYSIS ---

This page continues the Table of Contents from the previous page. The content is presented in a bilingual format; per the instructions, only the English translations are provided below.

| Section Number | Section Title | Page |
| :--- | :--- | :--- |
| 11.1 | Core Tasks | 12 |
| 11.2 | Suggested Repositories | 13 |
| 12 | Planning, Efficiency & Creativity Considerations | 13 |
| 13 | Selected Q&A Insights | 14 |
| 13.1 | Communities within File Communities | 14 |
| 13.2 | Building a Data Array for Agent Testing | 14 |
| 14 | Conclusion | 15 |

**Footer Information:**
* Page number: 3
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 4 ANALYSIS ---

**1 Introduction: The Goal of the Lecture and the Philosophy of the Course**

Dr. Yoram Segal opens the lecture by establishing the broader context of the course. The job market in high-tech has changed: companies today are looking for senior professionals with experience, and less for beginners (juniors). In the era of artificial intelligence and autonomous agents, the burden placed on every engineer is many times greater, and therefore the expectation is that a fresh graduate will already know how to think and work like an architect.

**Core Message of the Lecture**
The goal of the lesson is to provide tools that allow reading and improving large, unfamiliar codebases, while saving between 70% to 95% of the tokens we need to work with language models. This tool is Graph Theory and its application in software reverse engineering.

The lecturer emphasizes an important working principle: when using a Large Language Model (LLM), one must always add a personal contribution — to change, to expand, and to check the output — because this is the only way to truly learn and turn knowledge into a professional asset. This idea accompanies every assignment derived from the lecture.

**2 The Problem: The Context Window Bottleneck**

The central bottleneck of every language model is the Context Window. The amount of information that can be fed is limited, while the amount of information we want to inject is enormous. In previous lessons, we discussed the RAG solution, but it also has significant limitations.

**2.1 RAG Limitation: Vector Distance vs. Associative Connection**

The RAG method organizes information according to vector distances: words with similar meanings are located close to each other. However, this identifies only semantic similarity, and not an associative connection.

---
**Footer Information**
* Page number: 4
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 5 ANALYSIS ---

**Why Vector Distance Is Not Enough**

Consider the following set of words: Movie, Popcorn, Parking. Everyone immediately sees the story connecting them — going to the cinema. However, in the RAG vector space, there is no proximity between "Movie" and "Popcorn" or "Parking"; "Movie" is only close to "TV series." The associative connection — the human understanding — is missing.

Conclusion: To capture associative connections between data units, one must move from vector representation to graph representation.

**3 The Solution: The Three-Layer Architecture**

The lecturer presents a world built of three layers, each fulfilling a distinct role in transforming raw data into navigable knowledge:

**Table 1: The Three Layers of the Graph Knowledge System**

| Layer | Role |
| :--- | :--- |
| Files / Layers | All raw data: code, documents, video, audio |
| Grphify | Automatically builds a graph of the connections between files |
| Obsidian | Displays and navigates the graph in a visual and textual manner |

Grphify is a free tool that can be run directly from the CLI (for example, from Claude) or via a pipeline. It scans the files, identifies the connections between them, and creates a graph described in a graph.json file. Obsidian operates on top of this, providing a visual and textual representation that is convenient for both humans and AI agents.

**Footer Information:**
* Page number: 5
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 6 ANALYSIS ---

**4 Grphify vs. Obsidian: Division of Roles**

**4.1 The Strength of Grphify: Almost Free Analysis**
The main strength of Grphify is that it works almost without token costs. The reason is simple: if function A calls function B, a line is created between two nodes — and for this, there is no need for a language model at all, only for Python Abstract Syntax Tree (AST) analysis.

**Box: AST - Pure Logical Analysis**
Abstract Syntax Tree (AST) identifies the logic of the code itself — who calls whom, which conditions exist, and so on. This is a structural deduction that does not cost tokens. Only when we want to analyze video or audio files, or perform deep semantic content analysis, do we start paying for tokens, and therefore the tool asks in advance what the desired depth of research is.

**4.2 The Strength of Obsidian: The Wikipedia of the Project**
Obsidian works with Markdown files and breaks down any problem into an organized structure of linked files — similar to a directory structure. The result is similar to Wikipedia: every page contains links to other pages, and it is possible to navigate between ideas without limitation. The tool itself also identifies connections and gives them names and meanings.

**Box: The Wikipedia Analogy**
Like Wikipedia, where every reading leads to another link and another, Obsidian turns your collection of files into a knowledge space: it scans in parallel (Parallel Depth Scan), opens several simultaneous processes, and allows for convenient human work on the graph.

---
**Footer Information**
* Page number: 6
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 7 ANALYSIS ---

**5 Core Concepts: Information Flow in the System**

Obsidian has a "Vault" — the starting point of the project, which defines "who is playing." The user decides where to start scanning: an entire project or a specific folder (a decision that directly impacts token consumption). The flow is: Data ingestion -> Analysis by Grphify -> Graph creation (graph.json) -> Sending to Obsidian.

**Table 2: Hierarchy Concepts of the Knowledge Space**

| Concept | Meaning |
| :--- | :--- |
| Portfolio | The main work folder — the master header describing what is included |
| Domain | A field, like a "department" in a university (e.g., LaTeX) |
| Project | The operational unit: actual code, PRD, and work plans |

**Two Domains in the Same Project**
A single project may contain two different domains: a Python domain of agents, and alongside it, a LaTeX domain of project documents. Both live in the same tree, but they are separate fields.

**Secret: Graph over Scales**
The most important part of every file is the header at the top. The same idea is injected into scales: when Grphify is run on a collection of scales, they all describe a network of connections. This is the key to saving tokens — see the next section.

**Footer Information:**
* Page number: 7
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 8 ANALYSIS ---

**6 The Three Edge Types**

Grphify always presents nodes, and between the nodes are three types of connections, differentiated by their certainty levels:

**Table 3: Three Edge Types in the Graph and Their Certainty Levels**

| Edge Type | Meaning |
| :--- | :--- |
| Extracted | "Hard-coded": Function calls function — full certainty |
| Inferred | LLM inference from comments and text — partial certainty |
| Ambiguous | Ambiguous: "Something does not look right," requires human review |

**Ambiguous Edge**
Grphify might say: "This function was used once for stock calculation, and once for a LaTeX library. I am not sure — maybe it is the intended behavior, but it is worth checking." This is exactly the situation where human engineering attention is required.

**7 Token Efficiency**

The lecturer explains why regular work wastes tokens: before you have even written a single word in the prompt, the system already takes all your scales, extracts their descriptions, and injects them into the head of the context window. If you have tens or hundreds of scales, the window fills up even before you start.

**Hidden Waste**
As the number of scales grows, there is less and less room for the actual question. The window fills with information that is not relevant to the current query — and this is the central waste of tokens.

---
**Footer Information**
* Page number: 8
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 9 ANALYSIS ---

**7.1 The Graph Solution: Focused Retrieval**

In the graph-based method, the system first reads the query, understands the subject matter, and builds a focused graph itself. If the query concerns "pricing" in a project, it accesses the "pricing" node directly and extracts all connected nodes at once—without searching through all the scales.

**Comparison of Approaches**
Naive RAG introduces noise into the system: scale after scale, data after data, until the window is cluttered. The graph-based approach, by contrast, extracts only the relevant sub-tree. Both approaches are different ways of maintaining data—as RAG does not belong to a specific model, neither does the graph approach. There is no performance penalty—quite the opposite.

**8 Graph Theory: Centrality and Communities**

The lecturer emphasizes that he does not teach graph theory itself, but rather how to use it. Two central concepts serve the analysis:

**Centrality**
A node with high centrality is a node to which many connections arrive and from which many depart. The more it acts as a hub in the graph, the more lines point to it. There are designated algorithms for locating "central" nodes in the graph.

**Community**
A community is a group of nodes with many connections between them and few "bridges" to the outside. When the ratio between internal connections and external connections is high, it is considered a community. A node can be a file, a function, or any unit of information.

---
**Footer Information**
* Page number: 9
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 10 ANALYSIS ---

**8.1 What a Community Teaches Us About Architecture**

A community teaches us about the logical architecture of the system. The trivial example is a Full-Stack application: one community is the Frontend (Client) and another is the Backend (Server). Within each, there are many connections, but between them, there are only a few connections — a question and an answer.

**Architectural Red Flag**
Imagine a file with 50 functions where each one does something else without connection. This is a node with many functions — but if we see them "escaping" to other communities, this is evidence of poor design. Thus, the graph exposes faulty architecture.

In reverse engineering, the first step is a macro view: "who against whom" — where is the server, where is the client — and then performing a Drill-Down: opening every community into sub-communities, and so on.

**9 The "Lost in the Middle" Problem**

The lecturer emphasizes a critical phenomenon: in the context window, there is a "housing problem" (Lost in the Middle). The model gives weight to information at the beginning and information at the end, while information in the middle is weakened and may be forgotten or corrupted.

**Weak Information in the Middle**
The system remembers the beginning and the end well, but "loses" the middle. One of the reasons: sometimes questions asked in the middle hide a previous question, and the hidden information harms the quality of the answer.

**Practical Rule**
Although today there are windows of millions of tokens, our interest is that the segments be short. Always remember: the beginning of the prompt and the last sentence you write are the most important; everything else is an addition. In the exercises, you will be required to add token measurement and prove savings.

---
**Footer Information**
* Page number: 10
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 11 ANALYSIS ---

For large sets, it is recommended to perform a "Compaction" operation: it summarizes the content, attaches the beginning to the end, and "throws away" the middle, as the model performs poorly on it anyway. This operation is time-consuming but very efficient for the work.

**10 Architectural Analysis in Practice: Reading the Graph**
The analysis process begins with a macro view, and subsequently searches for communities, connections, and hubs.

| Hub |
| :--- |
| A Hub is a node through which everything passes — a bottleneck. A weak Hub (with few connections) is not dangerous, but a critical Hub through which all information flows is an architectural problem. |

**10.1 Bridges: Advantages and Disadvantages**
A Bridge allows information to reach two paths. Advantage: Redundancy and Fallback — if one path fails, information flows through another, and this is a more robust and reliable architecture. Disadvantage: Duplication, which may create load and consistency issues, as the same information may arrive at different times.

| Lack of Meaning in Physical Location |
| :--- |
| Remember the sanctification of the node: There is no meaning to the physical location of a node in the graph. Proximity or distance on the screen are matters of display convenience only. The only meaning is whether there is a line, and how many lines. The size of the circle (or background color) indicates the amount of information or the community it belongs to. |

**10.2 Alignment Between the PRD and Implementation**
One of the strengths of the approach: checking if the code written matches the Product Requirements Document (PRD). It is possible that Claude was "lazy" and implemented less than required, or "over-achieved" and implemented more. The graph reveals the lack of alignment between the documentation and the actual implementation, when there are not enough connections between the PRD pages and the implementation pages.

---
**Footer Information**
* Page number: 11
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 12 ANALYSIS ---

**The Architect Does Not Work in Real-Time**
It is necessary to re-run Grphify after every significant change, for example, by using a trigger in GitHub on every commit. The architect checks the product after it is completed, exactly as a submitted exercise is checked — not while writing. In a small project, there is no point in this; in a large project intended for production, it is mandatory.

**Authentication as a Path and Not as a Word**
The authentication process is shown as a path: UI (Submit) -> Controller -> Validation -> Database Read -> Approval. This connection point is a Single Point of Failure, which exposes both a risk of failure and potential load issues.

**11 Assignment (EX04): Reverse Engineering with AI Agents**

The assignment derived from the lecture requires taking a Python codebase that you are unfamiliar with, performing reverse engineering using graphs, and understanding what it does at the architectural level — not just every line of code, but how the code is planned and how it is built.

**11.1 Core Tasks**
1. **Code Cloning:** Downloading a repository from GitHub, or bringing personal code that is significant (with the lecturer's approval).
2. **Running Grphify:** Creating the graph, the index, and navigation pages (hot.md, etc.), and displaying them in Obsidian.
3. **Reverse Engineering:** Extracting a block diagram and an OOP schema of the classes. Do not settle for code that is already documented — the value is in the extraction of understanding.
4. **Building AI Agents:** An agent based on LangGraph or CrewAI for analysis, identification, and fixing of architectural bugs (such as Single Point of Failure and others).

---
**Footer Information**
* Page number: 12
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 13 ANALYSIS ---

5. **Improvement Loop:** The agent implements recommendations (e.g., splitting a large module), runs Grphify again, checks the result against stop conditions, and runs Unit Tests after every change.

| Multiplicity of Agents |
| :--- |
| Do not settle for one agent. It is better to have several agents, each an expert in its field: one expert in GitHub and code downloading, one in graph analysis and bug detection, and one in rewriting code based on the graph. This is where the orchestration of agents learned in the lesson comes in. |

**11.2 Suggested Repositories**

Table 4: Suggested code repositories, by complexity level

| Repository | Character |
| :--- | :--- |
| BugsInPy | Real bugs from the field - complex, requires environment adaptation |
| Academic exercise repositories | Simpler code snippets intended for practice |

| Pay Attention to the Environment |
| :--- |
| BugsInPy is a real repository, and therefore it is mandatory to work in a virtual environment. If the installation gets complicated (drivers, libraries) - do not get stuck; switch to a simpler repository. The choice of repository does not affect the grade; what affects it is what you learned and produced. |

**12 Planning, Efficiency & Creativity Considerations**

The lecturer requested to demonstrate token efficiency: presenting "before" vs. "after" (regular work vs. Grphify-assisted agent scanning, including token counts). Whoever did not succeed in saving - explain why.

---
**Footer Information**
* Page number: 13
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 14 ANALYSIS ---

**Budget and Time**
All tools run locally — these are small and lean tools. According to the lecturer's analysis, a pair working in a focused manner will finish the project in 5 hours of work. Anyone who feels they are approaching this time without progress — something is problematic and it is worth stopping and thinking. There is no point in turning the assignment into a final project.

**Creativity is the Core**
The base is written for everyone; anyone can feed the page to the model and get a solution. The real difference is what **you** bring yourselves: what additional uses, expansions, and insights. For example, Grphify can also be used for team management: mapping of R&D, HR, departments, and roles reveals problems in the organizational structure.

**13 Selected Q&A Insights**
At the end of the lecture, a practical discussion developed. Two main insights:

**13.1 The Communities of the Files**
The communities that Grphify identifies are the communities of the files, and the agents that use them. Also, a PRD document describing an agent will appear in the graph — the system builds everything into the graph, including identification of the communities.

**13.2 Building a Data Set for Agent Testing**
To the question of how to test an agent (for example, a good chatbot), the lecturer suggested a systematic process for building a data set (Dataset):
1. Generate 40,000-50,000 possible questions via a language model, with known answers.
2. Injection of intentional errors: choosing random letters and swapping them, to simulate typos, in increasing percentages.
3. Handling of multiple languages (for example, spoken Arabic, Palestinian, Egyptian, Syrian) — since it is not known in advance how the user will turn to the agent.
4. Building a Confusion Matrix: how many times the agent was correct versus how many errors.

---
**Footer Information**
* Page number: 14
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

--- PAGE 15 ANALYSIS ---

**Boxed Note: When does the "machine work"?**
The error rate is gradually increased until performance collapses (around 50% error rate for the agent). When reaching a logical number in the confusion matrix, one knows that the "machine works" and provides a reliable estimate of its error tolerance.

**14 Conclusion**
The lecture presented graph theory as a dual-purpose tool: first, to perform reverse engineering and understand code architecture on a scale of tens and hundreds of thousands of lines; and second, to save tokens dramatically by performing targeted retrieval from a graph instead of using a context window. The integration of Grphify (which builds the graph automatically, almost for free) with Obsidian (the visual engine) allows a graduate to think and work like an architect — and thus, according to Dr. Yoram Segal, the ability that will distinguish them in the market.

---
**Footer Information**
* Page number: 15
* Copyright notice: All rights reserved to Dr. Yoram Segal (c)

---

## Cross-Reference Clarifications

- **Page 7 → Page 8:** Page 8 explains how the graph-based approach described on page 7 serves as the key to saving tokens.
- **Page 10 → Page 11:** Page 11 provides the specific "Compaction" technique mentioned as a solution to the "Lost in the Middle" problem on page 10.
- **Page 12 → Page 2:** Page 2 contains the table of contents that lists the assignment details found on page 12.
- **Page 13 → Page 12:** Page 12 defines the core tasks for the assignment that page 13 discusses in terms of repository selection and environment setup.
