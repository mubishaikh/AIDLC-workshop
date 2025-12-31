# Ideation Portal - Unit of Work Story Map

## Overview
This document maps all 22 user stories to the 5 units of work. It provides a comprehensive view of how stories are organized within units and their implementation sequence.

---

## Story Distribution by Unit

### Unit 1: Idea Submission & Management
**Stories**: 5 stories
**Total Story Points**: ~13 points (estimated)

| Story # | Title | Priority | Complexity | Dependencies |
|---------|-------|----------|-----------|--------------|
| 1 | Submit New Idea | High | Simple | None |
| 2 | Save Idea as Draft | High | Simple | Story 1 |
| 3 | Add Contributors to Idea | Medium | Medium | Story 1 |
| 4 | View My Submitted Ideas | High | Simple | Story 1 |
| 5 | Edit Submitted Idea | Medium | Simple | Story 1 |

### Unit 2: Evaluation Framework
**Stories**: 4 stories
**Total Story Points**: ~13 points (estimated)

| Story # | Title | Priority | Complexity | Dependencies |
|---------|-------|----------|-----------|--------------|
| 6 | View Assigned Ideas for Evaluation | High | Simple | Unit 1 |
| 7 | Evaluate Idea with Quantifiable Metrics | High | Medium | Story 6 |
| 8 | Cannot See Other Evaluators' Scores During Evaluation Period | High | Medium | Story 7 |
| 9 | Add Comments and Justification to Evaluation | Medium | Simple | Story 7 |

### Unit 3: Dashboards & Leaderboards
**Stories**: 3 stories
**Total Story Points**: ~10 points (estimated)

| Story # | Title | Priority | Complexity | Dependencies |
|---------|-------|----------|-----------|--------------|
| 10 | View Real-Time Dashboard with All Ideas | High | Medium | Unit 1, Unit 2 |
| 11 | View Leaderboard Ranked by Composite Score | High | Medium | Story 10 |
| 12 | View Multi-Dimensional Comparative Analysis | Medium | Medium | Story 10 |

### Unit 4: Analytics & Recognition
**Stories**: 8 stories
**Total Story Points**: ~20 points (estimated)

| Story # | Title | Priority | Complexity | Dependencies |
|---------|-------|----------|-----------|--------------|
| 13 | View Analytics Dashboard with Top Ideas | High | Medium | Unit 1, Unit 2 |
| 14 | View Comparative Analysis Across Evaluation Criteria | Medium | Medium | Story 13 |
| 15 | Generate Executive Report | Medium | Medium | Story 13 |
| 16 | Automatically Identify Top 3 Ideas | High | Simple | Unit 2 |
| 17 | Award Digital Badges to Top 3 Ideas | High | Simple | Story 16 |
| 18 | Notify Winners of Recognition | High | Simple | Story 17 |
| 19 | Display Recognition Badges on User Profile | Medium | Simple | Story 17 |
| 20 | Display Recognition Badges on Leaderboard | Medium | Simple | Story 17 |

### Unit 5: Campaign Management
**Stories**: 2 stories
**Total Story Points**: ~6 points (estimated)

| Story # | Title | Priority | Complexity | Dependencies |
|---------|-------|----------|-----------|--------------|
| 21 | Create and Configure Evaluation Campaign | High | Medium | None |
| 22 | Monitor Campaign Evaluation Progress | High | Medium | Story 21 |

### Security Stories (Cross-Unit)
**Stories**: 3 stories
**Total Story Points**: ~9 points (estimated)

| Story # | Title | Priority | Complexity | Unit Dependencies |
|---------|-------|----------|-----------|-------------------|
| S1 | Implement Role-Based Access Control | High | Medium | All units |
| S2 | Implement User Authentication & Session Management | High | Medium | All units |
| S3 | Implement Audit Logging | High | Medium | All units |

---

## Story Implementation Sequence

### Phase 1: Foundation (Weeks 1-2)

**Unit 5: Campaign Management**
1. Story 21: Create and Configure Evaluation Campaign
   - Create campaign with dates and parameters
   - Assign panel members
   - Estimated: 1 week

2. Story 22: Monitor Campaign Evaluation Progress
   - Monitor evaluation progress
   - Track panel member status
   - Estimated: 1 week

**Unit 1: Idea Submission & Management**
1. Story 1: Submit New Idea
   - Basic idea submission form
   - Validation and storage
   - Estimated: 3 days

2. Story 2: Save Idea as Draft
   - Draft saving functionality
   - Resume editing from draft
   - Estimated: 2 days

3. Story 3: Add Contributors to Idea
   - Add colleagues as contributors
   - Contributor notifications
   - Estimated: 2 days

4. Story 4: View My Submitted Ideas
   - View user's ideas
   - Filter and sort
   - Estimated: 2 days

5. Story 5: Edit Submitted Idea
   - Edit submitted ideas
   - Validation and updates
   - Estimated: 1 day

**Security Stories (Parallel)**
- S1: Implement Role-Based Access Control
- S2: Implement User Authentication & Session Management
- S3: Implement Audit Logging

### Phase 2: Evaluation (Weeks 3-4)

**Unit 2: Evaluation Framework**
1. Story 6: View Assigned Ideas for Evaluation
   - Display assigned ideas
   - Show evaluation status
   - Estimated: 2 days

2. Story 7: Evaluate Idea with Quantifiable Metrics
   - Evaluation form with three metrics
   - Scoring and submission
   - Estimated: 3 days

3. Story 8: Cannot See Other Evaluators' Scores During Evaluation Period
   - Hide other scores during period
   - Reveal after period closes
   - Estimated: 2 days

4. Story 9: Add Comments and Justification to Evaluation
   - Comment fields for each metric
   - Overall comment field
   - Estimated: 1 day

### Phase 3: Visualization (Weeks 5-6)

**Unit 3: Dashboards & Leaderboards (Parallel)**
1. Story 10: View Real-Time Dashboard with All Ideas
   - Dashboard with all ideas and scores
   - Real-time updates via WebSocket
   - Estimated: 3 days

2. Story 11: View Leaderboard Ranked by Composite Score
   - Leaderboard ranking
   - Top ideas display
   - Estimated: 2 days

3. Story 12: View Multi-Dimensional Comparative Analysis
   - Comparative analysis views
   - Visual representations
   - Estimated: 2 days

**Unit 4: Analytics & Recognition (Parallel)**
1. Story 13: View Analytics Dashboard with Top Ideas
   - Analytics dashboard
   - Key metrics display
   - Estimated: 2 days

2. Story 14: View Comparative Analysis Across Evaluation Criteria
   - Comparative analysis
   - Heatmaps and distributions
   - Estimated: 2 days

3. Story 15: Generate Executive Report
   - Report generation
   - Export functionality
   - Estimated: 2 days

4. Story 16: Automatically Identify Top 3 Ideas
   - Identify top 3 by score
   - Tie-breaking logic
   - Estimated: 1 day

5. Story 17: Award Digital Badges to Top 3 Ideas
   - Badge creation and assignment
   - Badge storage
   - Estimated: 1 day

6. Story 18: Notify Winners of Recognition
   - Winner notifications
   - Email and in-app
   - Estimated: 1 day

7. Story 19: Display Recognition Badges on User Profile
   - Badge display on profile
   - Recognition history
   - Estimated: 1 day

8. Story 20: Display Recognition Badges on Leaderboard
   - Badge display on leaderboard
   - Visual indicators
   - Estimated: 1 day

---

## Story Dependencies

### Dependency Graph

```
Unit 5: Campaign Management
  ├→ Story 21: Create Campaign
  │   └→ Story 22: Monitor Progress
  │
Unit 1: Idea Submission
  ├→ Story 1: Submit Idea
  │   ├→ Story 2: Save Draft
  │   ├→ Story 3: Add Contributors
  │   ├→ Story 4: View My Ideas
  │   └→ Story 5: Edit Idea
  │
Unit 2: Evaluation
  ├→ Story 6: View Assigned Ideas
  │   ├→ Story 7: Evaluate Idea
  │   │   ├→ Story 8: Hide Other Scores
  │   │   └→ Story 9: Add Comments
  │
Unit 3: Dashboard
  ├→ Story 10: Real-Time Dashboard
  │   ├→ Story 11: Leaderboard
  │   └→ Story 12: Comparative Analysis
  │
Unit 4: Analytics & Recognition
  ├→ Story 13: Analytics Dashboard
  │   ├→ Story 14: Comparative Analysis
  │   └→ Story 15: Executive Report
  ├→ Story 16: Identify Top 3
  │   ├→ Story 17: Award Badges
  │   │   ├→ Story 18: Notify Winners
  │   │   ├→ Story 19: Display on Profile
  │   │   └→ Story 20: Display on Leaderboard
```

### Cross-Unit Dependencies

**Unit 1 → Unit 2:**
- Story 1 (Submit Idea) must complete before Story 6 (View Assigned Ideas)
- Ideas must exist before evaluation

**Unit 2 → Unit 3:**
- Story 7 (Evaluate Idea) must complete before Story 10 (Real-Time Dashboard)
- Scores must exist before dashboard display

**Unit 2 → Unit 4:**
- Story 7 (Evaluate Idea) must complete before Story 13 (Analytics Dashboard)
- Scores must exist before analytics

**Unit 4 → Unit 3:**
- Story 17 (Award Badges) should complete before Story 20 (Display on Leaderboard)
- Badges should be awarded before display

---

## Story Grouping by Epic

### Epic 1: Idea Submission & Management
- Story 1: Submit New Idea
- Story 2: Save Idea as Draft
- Story 3: Add Contributors to Idea
- Story 4: View My Submitted Ideas
- Story 5: Edit Submitted Idea

### Epic 2: Evaluation & Scoring
- Story 6: View Assigned Ideas for Evaluation
- Story 7: Evaluate Idea with Quantifiable Metrics
- Story 8: Cannot See Other Evaluators' Scores During Evaluation Period
- Story 9: Add Comments and Justification to Evaluation

### Epic 3: Dashboards & Leaderboards
- Story 10: View Real-Time Dashboard with All Ideas
- Story 11: View Leaderboard Ranked by Composite Score
- Story 12: View Multi-Dimensional Comparative Analysis

### Epic 4: Analytics & Reporting
- Story 13: View Analytics Dashboard with Top Ideas
- Story 14: View Comparative Analysis Across Evaluation Criteria
- Story 15: Generate Executive Report

### Epic 5: Recognition & Awards
- Story 16: Automatically Identify Top 3 Ideas
- Story 17: Award Digital Badges to Top 3 Ideas
- Story 18: Notify Winners of Recognition
- Story 19: Display Recognition Badges on User Profile
- Story 20: Display Recognition Badges on Leaderboard

### Epic 6: Campaign Management
- Story 21: Create and Configure Evaluation Campaign
- Story 22: Monitor Campaign Evaluation Progress

### Epic 7: Security & Compliance
- S1: Implement Role-Based Access Control
- S2: Implement User Authentication & Session Management
- S3: Implement Audit Logging

---

## Story Complexity Distribution

### By Unit
- **Unit 1**: 5 stories (2 Simple, 2 Simple, 1 Medium, 1 Simple, 1 Simple) = 5 Simple, 1 Medium
- **Unit 2**: 4 stories (1 Simple, 1 Medium, 1 Medium, 1 Simple) = 2 Simple, 2 Medium
- **Unit 3**: 3 stories (1 Medium, 1 Medium, 1 Medium) = 3 Medium
- **Unit 4**: 8 stories (1 Medium, 1 Medium, 1 Medium, 1 Simple, 1 Simple, 1 Simple, 1 Simple, 1 Simple) = 5 Simple, 3 Medium
- **Unit 5**: 2 stories (1 Medium, 1 Medium) = 2 Medium

### Overall Distribution
- **Simple**: 12 stories (55%)
- **Medium**: 10 stories (45%)
- **Complex**: 0 stories (0%)

---

## Story Priority Distribution

### By Priority
- **High**: 15 stories (68%)
- **Medium**: 7 stories (32%)
- **Low**: 0 stories (0%)

### By Unit
- **Unit 1**: 3 High, 2 Medium
- **Unit 2**: 3 High, 1 Medium
- **Unit 3**: 2 High, 1 Medium
- **Unit 4**: 4 High, 4 Medium
- **Unit 5**: 2 High, 0 Medium

---

## Story Estimation

### Estimated Story Points (Planning Poker)
- **Simple stories**: 2-3 points
- **Medium stories**: 5-8 points
- **Complex stories**: 13+ points

### Unit Effort Estimates
- **Unit 1**: ~13 points (2-3 weeks)
- **Unit 2**: ~13 points (2-3 weeks)
- **Unit 3**: ~10 points (2-3 weeks)
- **Unit 4**: ~20 points (3-4 weeks)
- **Unit 5**: ~6 points (1-2 weeks)

### Total Effort
- **Total Story Points**: ~62 points
- **Total Estimated Duration**: 13-18 weeks (sequential)
- **With Parallel Development**: 3.5-4.5 weeks

---

## Story Implementation Checklist

### Unit 1: Idea Submission & Management
- [ ] Story 1: Submit New Idea
- [ ] Story 2: Save Idea as Draft
- [ ] Story 3: Add Contributors to Idea
- [ ] Story 4: View My Submitted Ideas
- [ ] Story 5: Edit Submitted Idea

### Unit 2: Evaluation Framework
- [ ] Story 6: View Assigned Ideas for Evaluation
- [ ] Story 7: Evaluate Idea with Quantifiable Metrics
- [ ] Story 8: Cannot See Other Evaluators' Scores During Evaluation Period
- [ ] Story 9: Add Comments and Justification to Evaluation

### Unit 3: Dashboards & Leaderboards
- [ ] Story 10: View Real-Time Dashboard with All Ideas
- [ ] Story 11: View Leaderboard Ranked by Composite Score
- [ ] Story 12: View Multi-Dimensional Comparative Analysis

### Unit 4: Analytics & Recognition
- [ ] Story 13: View Analytics Dashboard with Top Ideas
- [ ] Story 14: View Comparative Analysis Across Evaluation Criteria
- [ ] Story 15: Generate Executive Report
- [ ] Story 16: Automatically Identify Top 3 Ideas
- [ ] Story 17: Award Digital Badges to Top 3 Ideas
- [ ] Story 18: Notify Winners of Recognition
- [ ] Story 19: Display Recognition Badges on User Profile
- [ ] Story 20: Display Recognition Badges on Leaderboard

### Unit 5: Campaign Management
- [ ] Story 21: Create and Configure Evaluation Campaign
- [ ] Story 22: Monitor Campaign Evaluation Progress

### Security Stories
- [ ] S1: Implement Role-Based Access Control
- [ ] S2: Implement User Authentication & Session Management
- [ ] S3: Implement Audit Logging

---

## Summary

**Total Stories**: 22 main stories + 3 security stories = 25 stories

**Story Distribution**:
- Unit 1: 5 stories (23%)
- Unit 2: 4 stories (18%)
- Unit 3: 3 stories (14%)
- Unit 4: 8 stories (36%)
- Unit 5: 2 stories (9%)

**Complexity**:
- Simple: 12 stories (55%)
- Medium: 10 stories (45%)
- Complex: 0 stories (0%)

**Priority**:
- High: 15 stories (68%)
- Medium: 7 stories (32%)
- Low: 0 stories (0%)

**Estimated Effort**: 62 story points, 3.5-4.5 weeks with parallel development

**Development Sequence**: Unit 5 & 1 → Unit 2 → Unit 3 & 4 (parallel)
