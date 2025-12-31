# Units Generation Plan - Ideation Portal

## Overview
This plan outlines the decomposition of the Ideation Portal into manageable units of work for parallel development. Based on the application design with 9 components and 6 services, the system will be decomposed into 5 units of work.

---

## Decomposition Strategy

### Proposed Units of Work

Based on the application design and service layer architecture, the system naturally decomposes into 5 units:

**Unit 1: Idea Submission & Management**
- Components: Idea Submission Component
- Services: Submission Service
- Stories: 1-5 (Submit, Draft, Contributors, View, Edit)
- Scope: Idea creation, draft management, contributor management

**Unit 2: Evaluation Framework**
- Components: Evaluation Component
- Services: Evaluation Service
- Stories: 6-9 (View Assigned, Evaluate, Independent Scoring, Comments)
- Scope: Evaluation process, scoring, comment management

**Unit 3: Dashboards & Leaderboards**
- Components: Dashboard Component, Leaderboard Component
- Services: Dashboard Service
- Stories: 10-12 (Dashboard, Leaderboard, Comparative Analysis)
- Scope: Real-time dashboard, leaderboard, comparative views

**Unit 4: Analytics & Recognition**
- Components: Analytics Component, Recognition Component
- Services: Analytics Service, Recognition Service
- Stories: 13-20 (Analytics, Reports, Top 3, Badges, Notifications, Display)
- Scope: Analytics, reporting, recognition, badge awards

**Unit 5: Campaign Management**
- Components: Campaign Component
- Services: Campaign Service
- Stories: 21-22 (Create Campaign, Monitor Progress)
- Scope: Campaign creation, panel assignment, progress monitoring

### Cross-Unit Components

**Shared Components** (used by multiple units):
- User Component - Authentication, authorization, user management
- Notification Component - Multi-channel notifications
- Campaign Component - Campaign context and validation

**Shared Services** (used by multiple units):
- All services depend on User Component for validation
- All services use Notification Component for notifications

---

## Units Generation Execution Plan

### Step 1: Define Unit Boundaries
- [ ] Identify component groupings for each unit
- [ ] Define unit responsibilities and scope
- [ ] Establish unit naming conventions
- [ ] Document unit purposes

### Step 2: Map Stories to Units
- [ ] Assign each user story to appropriate unit
- [ ] Verify all stories are assigned
- [ ] Identify cross-unit dependencies
- [ ] Document story-to-unit mapping

### Step 3: Identify Unit Dependencies
- [ ] Map dependencies between units
- [ ] Identify prerequisite units
- [ ] Establish integration points
- [ ] Document dependency constraints

### Step 4: Define Development Sequence
- [ ] Determine unit development order
- [ ] Identify parallel development opportunities
- [ ] Establish integration checkpoints
- [ ] Document critical path

### Step 5: Establish Unit Interfaces
- [ ] Define APIs between units
- [ ] Establish data contracts
- [ ] Document communication patterns
- [ ] Define error handling

### Step 6: Plan Unit Testing
- [ ] Define unit-level testing strategy
- [ ] Identify integration test points
- [ ] Plan end-to-end testing
- [ ] Document test coverage goals

### Step 7: Generate Unit Artifacts
- [ ] Create unit-of-work.md with unit definitions
- [ ] Create unit-of-work-dependency.md with dependency matrix
- [ ] Create unit-of-work-story-map.md with story mappings
- [ ] Validate unit completeness

---

## Decomposition Questions

Please answer the following questions to guide the units generation. Fill in the [Answer]: tag with your choice (A, B, C, D, or E for Other).

### Question 1
Should the units be organized by service/component or by user workflow?

A) By service/component - Each unit corresponds to a service (Submission, Evaluation, Dashboard, etc.)
B) By user workflow - Each unit represents a complete user journey (Submit→Evaluate→View Results)
C) By technical layer - Each unit represents a layer (API, Business Logic, Data Access)
D) Hybrid - Combination of service and workflow organization
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

### Question 2
Should units be developed sequentially or in parallel?

A) Sequential - Units developed one after another
B) Parallel - All units developed simultaneously
C) Hybrid - Some units in parallel, some sequential based on dependencies
D) Phased - Units grouped into phases (Phase 1, Phase 2, etc.)
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

### Question 3
How should shared components (User, Notification, Campaign) be handled?

A) Separate unit - Shared components as dedicated unit
B) Distributed - Shared components implemented in each unit that uses them
C) Centralized - Shared components implemented first, used by all units
D) Hybrid - Core shared components centralized, others distributed
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

### Question 4
Should each unit have its own database or share a single database?

A) Separate databases - Each unit has its own database
B) Single database - All units share one database
C) Hybrid - Shared database for core data, separate for unit-specific data
D) Event sourcing - Event log as source of truth
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

### Question 5
How should unit integration be managed?

A) API-based - Units communicate via REST APIs
B) Event-based - Units communicate via events
C) Direct - Units call each other directly
D) Hybrid - Mix of APIs and events
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

### Question 6
What is the expected team structure for development?

A) Single team - One team develops all units sequentially
B) Multiple teams - One team per unit, parallel development
C) Hybrid - Some units by single team, others by multiple teams
D) Flexible - Team structure determined per unit
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

### Question 7
Should units be independently deployable or deployed together?

A) Independent - Each unit deployed separately
B) Together - All units deployed as single release
C) Hybrid - Some units independent, others together
D) Phased - Units deployed in phases
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

### Question 8
How should unit dependencies be managed?

A) Strict - No circular dependencies, clear hierarchy
B) Flexible - Allow some circular dependencies if needed
C) Loose - Minimal dependency constraints
D) Event-driven - Dependencies managed via events
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Unit Artifacts to Generate

Once questions are answered, the following artifacts will be created:

### 1. unit-of-work.md
- Unit 1: Idea Submission & Management
- Unit 2: Evaluation Framework
- Unit 3: Dashboards & Leaderboards
- Unit 4: Analytics & Recognition
- Unit 5: Campaign Management

Each unit will include:
- Purpose and responsibilities
- Components and services
- Stories assigned
- Key features
- Development scope

### 2. unit-of-work-dependency.md
- Dependency matrix showing relationships between units
- Integration points and communication patterns
- Prerequisite units and critical path
- Development sequence recommendations

### 3. unit-of-work-story-map.md
- Mapping of all 22 user stories to units
- Story grouping within units
- Cross-unit story dependencies
- Story implementation sequence

---

## Next Steps

1. **Answer all decomposition questions** by filling in the [Answer]: tags above
2. **Review your answers** for consistency and clarity
3. **Approve this plan** to proceed with units generation
4. **Units artifacts will be created** in `aidlc-docs/inception/application-design/`

---

## Approval Checkpoint

Once you've answered all questions above, please confirm you're ready to proceed with units generation based on this plan.
