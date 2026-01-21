# Friction-Aware Learning System (Prototype)
## Team Hackathon Project — LEAP

This project was developed collaboratively as part of a hackathon team.  
I was an active team member involved in the project development process.

## Description / Overview

This repository contains a **prototype of a friction-aware learning system**, implemented as an interactive Streamlit application. The system adapts the learning environment dynamically by observing interaction signals, diagnosing areas of friction, and applying temporary, reversible adjustments to content presentation.

We focus on a **condition-based adaptation model**, where the system responds to learning conditions rather than learner identities, abilities, or backgrounds. This prototype is intended for **research and design purposes**, not as a production platform.

This README outlines both:

- What the **current codebase provides**, and  

- The **system model that our implementation follows**.

Any incomplete or conceptual functionality is clearly indicated.

---

## Purpose of the System

The project aims to demonstrate a practical model of adaptive learning based on **learning friction**.

We aim to answer four main questions:

- What observations does the system make?  

- How does it diagnose learning friction?  

- In what ways does it adapt the learning environment?  

- What are the boundaries of the system?  

All implementation choices made in this project follow this model.

---

## System Model Overview

### Observed Signals

The system **does not collect**:

- Learner identity  

- Ability  

- Background  

- Demographics or personal data  

Instead, we observe **signals generated during learning interactions**, which represent learning conditions rather than the learner themselves.

The prototype partially supports observation across the following categories.

---

#### A. Access & Environment Signals

**Purpose:** Identify whether learning can occur without technical issues.

Examples (partially implemented):

- Detecting device type (screen size, input mode)  

- Session reloads or interruptions  

- Success or fallback in content rendering  

Core question:  

> Are there disruptions before cognition can begin?

Prototype status:  

- Device detection is functional  

- Network diagnostics are limited  

- Media fallback handling is minimal

---

#### B. Interaction & Behavior Signals

**Purpose:** Understand how learners navigate steps in the lesson.

Examples (partially implemented):

- Time spent on each step  

- Navigation between steps  

- Repeated exposure to content  

Core question:  

> Is the learner confused, stuck, moving too fast, or disengaged?

Prototype status:  

- Time-based signals are tracked  

- Navigation patterns are partially observed  

- Fine-grained interaction logging is limited

---

#### C. Cognitive Load Proxy Signals

 

**Purpose:** Estimate mental strain without inferring ability.

 

Examples (conceptual, limited implementation):

 

- Unusually long response times  

- Repeated difficulties with related steps  

- Mid-step abandonment  

 

Core question:  

> Is the pacing or structure overwhelming?

 

Prototype status:  

- Time-based proxies exist  

- Error clustering and task abandonment are not fully implemented

 

---

 

#### D. Motivation & Regulation Signals

 

**Purpose:** Detect decreasing momentum or self-regulation.

 

Examples (conceptual):

 

- Shortened sessions  

- Delayed returns after difficulty  

- Avoidance of optional content  

 

Core question:  

> Is the learner losing direction or perceived value?

 

Prototype status:  

- Session continuity is observable  

- Long-term motivation tracking is not implemented

 

---

 

#### E. Application & Transfer Signals

 

**Purpose:** Assess whether learning generalizes beyond practice.

 

Examples (conceptual):

 

- Failure when context changes  

- Difficulty with open-ended prompts  

- Success only in repeated tasks  

 

Core question:  

> Is learning brittle or transferable?

 

Prototype status:  

- Conceptual only  

- No robust transfer evaluation implemented yet

 

---

 

#### F. Explicit Learner-Provided Signals (Optional)

 

**Purpose:** Reduce friction by incorporating learner preferences.

 

Examples (implemented):

 

- Preferred explanation style  

- Accessibility settings  

- Optional self-reported confusion  

 

Core question:  

> How can friction be reduced without identifying the learner?

 

Prototype status:  

- Preference collection UI is functional  

- Preferences affect content generation at a basic level

 

---

 

## Diagnosing Learning Friction

 

Diagnosis is **condition-based, temporary, and explainable**.

 

We use a **two-layer diagnosis model** that aligns with the intended system architecture.

 

---

 

### Locked Friction Palette

 

All frictions are mapped to one of the following five categories:

 

1. Access friction  

2. Cognitive load friction  

3. Regulation & motivation friction  

4. Interaction & feedback friction  

5. Transfer & meaning friction  

 

No learner labels are assigned at any stage.

 

Prototype status:  

- Palette is conceptually defined  

- Partial mapping exists in reasoning modules  

- Coverage is incomplete but structurally enforced

 

---

 

### Layer 1 — Friction Detection (Coarse)

 

**Characteristics:**

 

- Continuous evaluation  

- Short time windows  

- Boolean activation (true/false)  

- Pattern-based, not event-based  

 

**Output:**  

- Temporary friction activation map  

 (e.g., access = true, cognitive load = false)

 

Prototype status:  

- Implemented at a basic level  

- Detection heuristics are simple  

- No persistent state is stored

 

---

 

### Layer 2 — Friction-Specific Diagnosis (Targeted)

 

**Characteristics:**

 

- Runs only for detected frictions  

- Determines the cause and extent of friction  

- Separate module per friction type  

 

**Output:**  

- Extent-based friction profile  

 (e.g., text stable, video unstable; moderate overload)

 

Prototype status:  

- Diagnosis scaffolding exists  

- Limited, heuristic-based implementation  

- Extent modeling is minimal

 

---

 

## Adapting the Learning Environment

 

Adaptation occurs **after diagnosis**. The system adapts **learning conditions**, not learners.

 

---

 

### Adaptation Principles

 

- Triggered only after diagnosis  

- Local in scope  

- Reversible  

- Continuously monitored  

- Removed once friction subsides  

 

Prototype status:  

- Adaptation logic exists  

- Reversibility is implicit, not automated  

- Continuous monitoring is limited

 

---

 

### Adaptation Logic (Examples)

 

- Access friction → adjust content delivery format  

- Cognitive load → adjust pacing or scaffolding  

- Motivation → reframe goals or feedback  

- Interaction → clarify correction structure  

- Transfer → add contextual variation  

 

Prototype status:  

- Cognitive load and access adjustments are partially implemented  

- Other mappings remain conceptual or minimal

 

---

 

### Closed Loop

 

Intended loop:  

 

observe → diagnose → adapt → observe  

 

Prototype status:  

- Concept exists  

- Feedback tightening is incomplete

 

---

 

## Architecture / Workflow

 

### High-Level Workflow

 

1. User enters the Streamlit application  

2. Optional preferences are collected  

3. Learning session begins  

4. Signals are collected  

5. Friction detection evaluates patterns  

6. Diagnosis modules analyze active frictions  

7. Content generator adjusts steps  

8. UI renders adapted steps  

9. The loop continues

 

---

 

### Code Architecture

 

IB League/  

├── app.py — main workflow and orchestration  

├── ui/ — user interface  

├── signals/ — signal collection and schemas  

├── reasoning/ — friction diagnosis and adaptation  

├── content/ — learning content  

├── util/ — device and timing tools  

└── .streamlit/ — Streamlit configuration  

 

Rules:  

- UI does not diagnose  

- Diagnosis does not render content  

- Adaptation does not store learner attributes

 

---

 

## Features That Work

 

- Streamlit interactive UI  

- Preference collection  

- Basic signal collection  

- Prototype friction detection  

- Simple adaptive content generation  

- Modular architecture

 

---

 

## Features Not Fully Implemented

 

- Robust signal logging  

- Fine-grained interaction tracking  

- Transfer and application diagnostics  

- Long-term motivation modeling  

- Automatic adaptation rollback  

- Testing framework  

- Production deployment tools



## References

This project draws on established research and reports in learning science, adaptive learning systems, and the economics of education. Key sources include:

OECD. The Economic Impacts of Learning Losses. OECD Publishing, 2020.
— Analysis of long-term GDP and productivity losses caused by learning gaps.

UNESCO. Out-of-School Children and Educational Gaps Cost the Global Economy Trillions Annually. UNESCO, 2024.
— Global overview of education exclusion and economic impact.

Teachers College, Columbia University. The Cost of Inadequate Education to Society. 2005.
— Foundational analysis of economic, health, and social costs of educational failure.

Carnegie Learning. Research on Adaptive and Personalized Learning Systems.
— Empirical studies showing improvements in engagement and learning outcomes.

OECD Education Working Papers. Personalised Learning and the Role of Technology.
— Policy-oriented discussion on personalization, equity, and system-level design.

Kwak, M. The Effectiveness of AI-Driven Tools in Improving Student Outcomes.
International Association for Computer Information Systems (IACIS), 2025.
— Meta-analysis of AI-based adaptive learning systems across contexts.

VanLehn, K. The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems.
Educational Psychologist, 2011.
— Comparative study of adaptive feedback and learning support mechanisms.

Bloom, B. S. The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring.
Educational Researcher, 1984.
— Classic work motivating adaptive and mastery-based learning approaches.

## Notes on AI Use

AI tools (including large language models) were used to assist with research synthesis, prototyping, and system design exploration. All outputs were reviewed, adapted, and integrated by the team. No AI system was used to evaluate learner ability or make high-stakes educational decisions.
