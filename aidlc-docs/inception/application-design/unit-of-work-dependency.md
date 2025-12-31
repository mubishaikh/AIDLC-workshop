# Ideation Portal - Unit of Work Dependencies

## Overview
This document defines the dependencies, relationships, and communication patterns between the 5 units of work. It provides a comprehensive view of how units integrate and depend on each other.

---

## Unit Dependency Matrix

### Dependency Table

| Unit | Depends On | Depended On By | Relationship Type | Critical |
|------|-----------|----------------|-------------------|----------|
| Unit 1: Submission | Shared (User, Notification) | Unit 2, 3, 4 | Data source | Yes |
| Unit 2: Evaluation | Unit 1, Unit 5, Shared | Unit 3, 4 | Processing | Yes |
| Unit 3: Dashboard | Unit 1, Unit 2, Unit 5 | Unit 4 | Aggregation | Yes |
| Unit 4: Analytics | Unit 1, Unit 2, Unit 5 | Unit 3 | Analysis | No |
| Unit 5: Campaign | Shared (User, Notification) | Unit 1, 2, 3, 4 | Orchestration | Yes |

---

## Detailed Unit Relationships

### Unit 1: Idea Submission & Management

**Depends On:**
- **User Component** (shared) - Validates submitter and contributors
- **Notification Component** (shared) - Sends notifications to contributors

**Depended On By:**
- **Unit 2: Evaluation** - Retrieves idea details for evaluation
- **Unit 3: Dashboard** - Displays ideas with scores
- **Unit 4: Analytics** - Analyzes ideas

**Communication Pattern:**
```
Unit 1 (Submission)
  ├→ User Component (validation)
  ├→ Notification Component (async)
  │
  ├→ Unit 2 (read ideas)
  ├→ Unit 3 (read ideas)
  └→ Unit 4 (read ideas)
```

**Data Flow:**
- Submitter creates idea → Unit 1 stores idea
- Contributors added → Notification sends notifications
- Unit 2 retrieves idea details → Unit 2 Evaluation Component
- Unit 3 aggregates ideas → Unit 3 Dashboard Component
- Unit 4 analyzes ideas → Unit 4 Analytics Component

**Integration Points:**
- API: `GET /ideas/{ideaId}` - Retrieve idea details
- API: `GET /ideas` - List ideas for campaign
- Event: `IdeaSubmitted` - Idea submission event
- Event: `ContributorAdded` - Contributor added event

**Critical Dependency**: Yes - All other units depend on idea data

---

### Unit 2: Evaluation Framework

**Depends On:**
- **Unit 1: Submission** - Retrieves idea details
- **Unit 5: Campaign** - Validates evaluation period and panel assignments
- **User Component** (shared) - Validates panel members
- **Notification Component** (shared) - Sends evaluation notifications

**Depended On By:**
- **Unit 3: Dashboard** - Retrieves current scores
- **Unit 4: Analytics** - Retrieves scores for analysis

**Communication Pattern:**
```
Unit 2 (Evaluation)
  ├→ Unit 1 (read ideas)
  ├→ Unit 5 (validate period)
  ├→ User Component (validation)
  ├→ Notification Component (async)
  │
  ├→ Unit 3 (provide scores)
  └→ Unit 4 (provide scores)
```

**Data Flow:**
- Panel member submits evaluation → Unit 2 stores scores
- Evaluation period closes → Scores aggregated
- Unit 3 requests scores → Unit 2 returns current scores
- Unit 4 requests scores → Unit 2 returns all scores
- Unit 4 identifies top 3 → Unit 2 provides scores

**Integration Points:**
- API: `GET /campaigns/{campaignId}/evaluation-period` - Check period status
- API: `GET /ideas/{ideaId}/aggregated-scores` - Get aggregated scores
- Event: `EvaluationSubmitted` - Evaluation submission event
- Event: `EvaluationPeriodClosed` - Period closure event
- WebSocket: Real-time score updates

**Critical Dependency**: Yes - Units 3 and 4 depend on evaluation scores

**Critical Constraint**: 
- During evaluation period: Other evaluators' scores are hidden
- After evaluation period: Aggregated scores are revealed

---

### Unit 3: Dashboard & Leaderboards

**Depends On:**
- **Unit 1: Submission** - Retrieves idea details
- **Unit 2: Evaluation** - Retrieves current scores
- **Unit 5: Campaign** - Retrieves campaign context

**Depended On By:**
- **Unit 4: Analytics** - For badge display coordination

**Communication Pattern:**
```
Unit 3 (Dashboard)
  ├→ Unit 1 (read ideas)
  ├→ Unit 2 (read scores, real-time)
  ├→ Unit 5 (read campaign)
  │
  └→ Unit 4 (provide badge display)
```

**Data Flow:**
- User requests dashboard → Unit 3 aggregates data
- Evaluation submitted → Unit 2 notifies Unit 3
- Unit 3 receives real-time update → Updates cache
- Unit 3 broadcasts update → All connected clients receive update
- Unit 4 awards badges → Unit 3 displays badges

**Integration Points:**
- API: `GET /dashboard` - Get dashboard data
- API: `GET /ideas/{ideaId}/with-scores` - Get idea with scores
- WebSocket: `WS /dashboard/subscribe` - Subscribe to real-time updates
- Event: `EvaluationSubmitted` - Triggers dashboard update
- Event: `BadgeAwarded` - Triggers badge display update

**Real-Time Update Flow:**
```
Evaluation Submitted (Unit 2)
    ↓
Unit 2 stores score
    ↓
Unit 2 publishes event
    ↓
Unit 3 receives event
    ↓
Unit 3 updates cache
    ↓
Unit 3 broadcasts via WebSocket
    ↓
Clients receive real-time update
```

**Performance Requirement**: Dashboard loads in 2 seconds, updates within 5 seconds

---

### Unit 4: Analytics & Recognition

**Depends On:**
- **Unit 1: Submission** - Retrieves idea and contributor details
- **Unit 2: Evaluation** - Retrieves scores for analysis
- **Unit 5: Campaign** - Retrieves campaign context
- **Notification Component** (shared) - Sends winner notifications
- **User Component** (shared) - Validates users

**Depended On By:**
- **Unit 3: Dashboard** - For badge display on leaderboard

**Communication Pattern:**
```
Unit 4 (Analytics & Recognition)
  ├→ Unit 1 (read ideas, contributors)
  ├→ Unit 2 (read scores)
  ├→ Unit 5 (read campaign)
  ├→ Notification Component (async)
  ├→ User Component (validation)
  │
  └→ Unit 3 (provide badges)
```

**Data Flow:**
- Administrator requests analytics → Unit 4 aggregates data
- Evaluation period closes → Unit 4 identifies top 3
- Unit 4 awards badges → Stores badge data
- Unit 4 sends notifications → Notification Component
- Unit 3 displays badges → Unit 4 provides badge data
- Unit 4 generates report → Returns report file

**Integration Points:**
- API: `GET /analytics/dashboard` - Get analytics dashboard
- API: `POST /recognition/identify-top-3` - Identify top 3
- API: `POST /recognition/award-badges` - Award badges
- API: `GET /ideas/{ideaId}/badges` - Get badges for display
- Event: `EvaluationPeriodClosed` - Triggers recognition workflow
- Event: `BadgeAwarded` - Notifies Unit 3 for display

**Recognition Workflow:**
```
Evaluation Period Closes (Unit 5)
    ↓
Unit 4 identifies top 3 (Unit 2 scores)
    ↓
Unit 4 awards badges (Unit 1 contributors)
    ↓
Unit 4 sends notifications (Notification Component)
    ↓
Unit 3 displays badges (Unit 4 badge data)
```

**Non-Critical Dependency**: Analytics can be generated independently, recognition depends on evaluation completion

---

### Unit 5: Campaign Management

**Depends On:**
- **User Component** (shared) - Validates administrators and panel members
- **Notification Component** (shared) - Sends campaign notifications

**Depended On By:**
- **Unit 1: Submission** - Associates ideas with campaigns
- **Unit 2: Evaluation** - Validates evaluation period
- **Unit 3: Dashboard** - Provides campaign context
- **Unit 4: Analytics** - Provides campaign context

**Communication Pattern:**
```
Unit 5 (Campaign)
  ├→ User Component (validation)
  ├→ Notification Component (async)
  │
  ├→ Unit 1 (campaign association)
  ├→ Unit 2 (period validation)
  ├→ Unit 3 (campaign context)
  └→ Unit 4 (campaign context)
```

**Data Flow:**
- Administrator creates campaign → Unit 5 stores campaign data
- Campaign assigns panel members → Sends notifications
- Unit 1 submits idea → Associates with current campaign
- Unit 2 checks period → Unit 5 validates
- Unit 3 displays ideas → Filtered by campaign
- Unit 4 analyzes ideas → Filtered by campaign

**Integration Points:**
- API: `POST /campaigns` - Create campaign
- API: `GET /campaigns/{campaignId}` - Get campaign details
- API: `GET /campaigns/{campaignId}/evaluation-period` - Check period status
- Event: `CampaignCreated` - Campaign creation event
- Event: `EvaluationPeriodClosed` - Period closure event

**Critical Dependency**: Yes - Provides campaign context and period validation to all units

---

## Dependency Levels

### Level 0: Shared Components (Foundational)
- **User Component** - Authentication, authorization, user management
- **Notification Component** - Multi-channel notifications

### Level 1: Orchestration Unit
- **Unit 5: Campaign Management** - Provides campaign context and period validation
- Depends on: Shared components only
- Depended on by: All other units

### Level 2: Data Unit
- **Unit 1: Idea Submission & Management** - Provides idea data
- Depends on: Shared components, Unit 5 (campaign context)
- Depended on by: Units 2, 3, 4

### Level 3: Processing Unit
- **Unit 2: Evaluation Framework** - Provides evaluation scores
- Depends on: Unit 1 (idea data), Unit 5 (period validation), Shared components
- Depended on by: Units 3, 4

### Level 4: Aggregation Units
- **Unit 3: Dashboard & Leaderboards** - Aggregates and displays data
- **Unit 4: Analytics & Recognition** - Analyzes data and awards recognition
- Depend on: Units 1, 2, 5
- Depended on by: Each other (for badge display)

---

## Development Sequence

### Recommended Development Order

**Phase 1: Foundation (Weeks 1-2)**
```
Unit 5: Campaign Management
  └→ Provides campaign context for all units
  
Unit 1: Idea Submission & Management
  └→ Provides idea data for all units
```

**Phase 2: Evaluation (Weeks 3-4)**
```
Unit 2: Evaluation Framework
  ├→ Depends on: Unit 1 (ideas), Unit 5 (campaign)
  └→ Provides: Evaluation scores for Units 3, 4
```

**Phase 3: Visualization (Weeks 5-6)**
```
Unit 3: Dashboard & Leaderboards (parallel)
  ├→ Depends on: Unit 1 (ideas), Unit 2 (scores), Unit 5 (campaign)
  └→ Provides: Display for badges from Unit 4

Unit 4: Analytics & Recognition (parallel)
  ├→ Depends on: Unit 1 (ideas), Unit 2 (scores), Unit 5 (campaign)
  └→ Provides: Badges for display in Unit 3
```

### Parallel Development Opportunities

**Can be developed in parallel:**
- Unit 1 (Submission) and Unit 5 (Campaign) - Independent, both foundational
- Unit 3 (Dashboard) and Unit 4 (Analytics) - Both depend on Unit 2, can start together after Unit 2

**Must be sequential:**
- Unit 5 (Campaign) before Unit 2 (Evaluation) - Campaign provides period validation
- Unit 1 (Submission) before Unit 2 (Evaluation) - Evaluation needs ideas
- Unit 2 (Evaluation) before Unit 3 (Dashboard) - Dashboard needs scores
- Unit 2 (Evaluation) before Unit 4 (Analytics) - Analytics needs scores

### Critical Path
```
Unit 5 (Campaign) → Unit 1 (Submission) → Unit 2 (Evaluation) → Unit 3 & 4 (Dashboard & Analytics)
```

**Total Duration**: 3.5-4.5 weeks with parallel development

---

## Integration Points

### Unit 1 ↔ Unit 2: Idea Data
**Direction**: Unit 1 → Unit 2
**Type**: Synchronous API calls
**APIs**:
- `GET /ideas/{ideaId}` - Retrieve idea details
- `GET /ideas` - List ideas for campaign
**Events**:
- `IdeaSubmitted` - Idea submission event
- `ContributorAdded` - Contributor added event

### Unit 2 ↔ Unit 3: Evaluation Scores (Real-Time)
**Direction**: Unit 2 → Unit 3
**Type**: Real-time WebSocket + Synchronous API
**APIs**:
- `GET /ideas/{ideaId}/aggregated-scores` - Get aggregated scores
- `GET /ideas/{ideaId}/evaluation-progress` - Get evaluation progress
**Events**:
- `EvaluationSubmitted` - Triggers dashboard update
- `EvaluationPeriodClosed` - Triggers score revelation
**WebSocket**:
- Real-time score updates within 5 seconds

### Unit 2 ↔ Unit 4: Evaluation Scores (Batch)
**Direction**: Unit 2 → Unit 4
**Type**: Synchronous API calls
**APIs**:
- `GET /ideas/{ideaId}/aggregated-scores` - Get aggregated scores
- `GET /ideas` - List all ideas with scores
**Events**:
- `EvaluationPeriodClosed` - Triggers analytics and recognition

### Unit 3 ↔ Unit 4: Badge Display
**Direction**: Unit 4 → Unit 3
**Type**: Synchronous API calls
**APIs**:
- `GET /ideas/{ideaId}/badges` - Get badges for display
- `GET /users/{userId}/badges` - Get user's badges
**Events**:
- `BadgeAwarded` - Triggers badge display update

### Unit 5 ↔ All Units: Campaign Context
**Direction**: Unit 5 → All Units
**Type**: Synchronous API calls
**APIs**:
- `GET /campaigns/{campaignId}` - Get campaign details
- `GET /campaigns/{campaignId}/evaluation-period` - Check period status
- `GET /campaigns/{campaignId}/status` - Get campaign status
**Events**:
- `CampaignCreated` - Campaign creation event
- `EvaluationPeriodClosed` - Period closure event

---

## Communication Patterns

### Synchronous Communication
Used for immediate operations where caller waits for response:
- Unit 1 → User Component (validation)
- Unit 2 → Unit 5 (period validation)
- Unit 3 → Unit 2 (score retrieval)
- Unit 4 → Unit 2 (score retrieval)

### Asynchronous Communication
Used for background operations where caller doesn't wait:
- Unit 1 → Notification Component (send notifications)
- Unit 2 → Notification Component (send notifications)
- Unit 4 → Notification Component (send winner notifications)
- Unit 5 → Notification Component (send campaign notifications)

### Real-Time Communication
Used for live updates via WebSocket:
- Unit 2 → Unit 3 (real-time score updates)
- Unit 3 ↔ Clients (real-time dashboard updates)

### Event-Driven Communication
Used for workflow orchestration:
- Evaluation Submitted → Dashboard Update → Broadcast
- Evaluation Period Closed → Recognition Trigger → Badge Award → Notification

---

## Deployment Strategy

### Independent Deployment
Each unit can be deployed independently:
- Unit 1: Idea Submission & Management
- Unit 5: Campaign Management

### Dependent Deployment
Units must be deployed in order:
- Unit 5 (Campaign) before Unit 2 (Evaluation)
- Unit 1 (Submission) before Unit 2 (Evaluation)
- Unit 2 (Evaluation) before Unit 3 (Dashboard)
- Unit 2 (Evaluation) before Unit 4 (Analytics)

### Coordinated Deployment
Units should be deployed together:
- Unit 3 (Dashboard) and Unit 4 (Analytics) - For badge display coordination

### Deployment Order
1. Shared Components (User, Notification)
2. Unit 5 (Campaign Management)
3. Unit 1 (Idea Submission)
4. Unit 2 (Evaluation Framework)
5. Unit 3 (Dashboard) and Unit 4 (Analytics) - In parallel

---

## Testing Strategy

### Unit-Level Testing
- Test each unit in isolation
- Mock dependencies
- Test error handling

### Integration Testing
- Test unit interactions
- Test data flow between units
- Test error propagation
- Test real-time updates

### End-to-End Testing
- Test complete workflows
- Test all units working together
- Test real-time updates
- Test recognition workflow

### Dependency Testing
- Verify dependencies are correctly implemented
- Test dependency injection
- Test circular dependency prevention

---

## Scalability Considerations

### Independent Scaling
These units can be scaled independently:
- **Unit 3: Dashboard** - Scale for concurrent users
- **Unit 4: Analytics** - Scale for report generation

### Shared Scaling
These units should scale together:
- **Unit 1 + Unit 2** - Both handle user submissions
- **Unit 5 + Unit 2** - Campaign orchestrates evaluation

### Database Scaling
- **Read-heavy units** (Unit 3, Unit 4) - Use read replicas
- **Write-heavy units** (Unit 1, Unit 2) - Use write optimization
- **Shared data** (Unit 5) - Use connection pooling

---

## Circular Dependency Analysis

**No circular dependencies detected:**
- All dependencies flow in one direction
- Units can be tested in isolation
- No deadlock risks
- Clean dependency hierarchy

**Dependency Flow:**
```
Shared Components (User, Notification)
    ↓
Unit 5 (Campaign)
    ↓
Unit 1 (Submission)
    ↓
Unit 2 (Evaluation)
    ↓
Unit 3 (Dashboard) ← → Unit 4 (Analytics)
```

---

## Summary

**Unit Dependencies:**
- Unit 1: Depends on Shared, Unit 5
- Unit 2: Depends on Unit 1, Unit 5, Shared
- Unit 3: Depends on Unit 1, Unit 2, Unit 5
- Unit 4: Depends on Unit 1, Unit 2, Unit 5, Shared
- Unit 5: Depends on Shared only

**Critical Path**: Unit 5 → Unit 1 → Unit 2 → Unit 3 & 4

**Development Duration**: 3.5-4.5 weeks with parallel development

**Key Success Factors**:
- Clear unit boundaries and interfaces
- Effective parallel development coordination
- Robust integration testing
- Real-time update performance
- Recognition workflow reliability
