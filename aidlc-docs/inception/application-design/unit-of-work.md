# Ideation Portal - Units of Work

## Overview
The Ideation Portal is decomposed into 5 units of work for parallel development. Each unit represents a logical grouping of components, services, and stories that can be developed independently while maintaining clear integration points.

**Decomposition Strategy**: Hybrid approach combining service/component organization with user workflow considerations.

**Development Approach**: Hybrid parallel development with dependency-based sequencing.

**Deployment Strategy**: Independent deployment per unit with coordinated releases.

---

## Unit 1: Idea Submission & Management

**Purpose**: Enable employees to submit innovative ideas with draft saving and contributor management

**Scope**: Core idea submission workflow, draft management, and collaboration features

### Components
- **Idea Submission Component** (primary)
- **User Component** (shared - validation)
- **Notification Component** (shared - notifications)

### Services
- **Submission Service** - Orchestrates submission workflow

### User Stories Assigned
- Story 1: Submit New Idea
- Story 2: Save Idea as Draft
- Story 3: Add Contributors to Idea
- Story 4: View My Submitted Ideas
- Story 5: Edit Submitted Idea

### Key Features
1. **Idea Submission**
   - Structured input fields (title, description, expected impact)
   - Form validation with helpful error messages
   - Timestamp and attribution
   - Confirmation with idea ID

2. **Draft Management**
   - Save incomplete ideas as drafts
   - Resume editing from draft
   - Draft retention for 30 days
   - Draft deletion with confirmation

3. **Contributor Management**
   - Add colleagues as contributors
   - Searchable employee list
   - Multiple contributor support
   - Contributor notifications
   - All contributors receive recognition if idea wins

4. **Idea Viewing**
   - View all submitted ideas with status
   - Filter by status
   - Sort by submission date or status
   - View idea details and contributors
   - Edit ideas before evaluation begins

### Data Entities
- Idea (id, title, description, expectedImpact, submitterId, contributors, status, createdAt, updatedAt)
- Draft (id, userId, ideaData, createdAt, updatedAt)
- Contributor (ideaId, userId, addedAt)

### APIs/Interfaces
- `POST /ideas` - Submit new idea
- `POST /drafts` - Save draft
- `GET /drafts/{draftId}` - Retrieve draft
- `PUT /drafts/{draftId}` - Update draft
- `DELETE /drafts/{draftId}` - Delete draft
- `POST /ideas/{ideaId}/contributors` - Add contributor
- `DELETE /ideas/{ideaId}/contributors/{userId}` - Remove contributor
- `GET /ideas/{ideaId}` - Get idea details
- `GET /my-ideas` - Get user's ideas
- `PUT /ideas/{ideaId}` - Edit idea

### Dependencies
- **Depends On**: User Component (validation), Notification Component (notifications)
- **Depended On By**: Evaluation Unit, Dashboard Unit, Analytics Unit, Recognition Unit
- **Integration Points**: 
  - User validation for submitter and contributors
  - Notification sending to contributors
  - Idea data provided to evaluation and dashboard units

### Development Complexity
- **Complexity Level**: Medium
- **Estimated Effort**: 2-3 weeks
- **Team Size**: 2-3 developers
- **Key Challenges**: Draft persistence, contributor management, validation

### Testing Strategy
- Unit tests for submission logic
- Integration tests with User and Notification components
- End-to-end tests for complete submission workflow
- Test coverage target: 85%+

### Deployment Considerations
- Independent deployment possible
- Database schema: ideas, drafts, contributors tables
- No external dependencies for core functionality
- Can be deployed before other units

---

## Unit 2: Evaluation Framework

**Purpose**: Enable panel members to independently evaluate ideas using quantifiable metrics

**Scope**: Evaluation process, scoring, comment management, and score visibility control

### Components
- **Evaluation Component** (primary)
- **Campaign Component** (shared - period validation)
- **User Component** (shared - validation)
- **Notification Component** (shared - notifications)

### Services
- **Evaluation Service** - Orchestrates evaluation workflow

### User Stories Assigned
- Story 6: View Assigned Ideas for Evaluation
- Story 7: Evaluate Idea with Quantifiable Metrics
- Story 8: Cannot See Other Evaluators' Scores During Evaluation Period
- Story 9: Add Comments and Justification to Evaluation

### Key Features
1. **Evaluation Assignment**
   - View assigned ideas for evaluation
   - Display evaluation status (Not Started, In Progress, Completed)
   - Show evaluation progress percentage
   - Display evaluation deadline

2. **Scoring System**
   - Three metrics: Feasibility (1-10), Impact (1-10), Innovation (1-10)
   - Visual scale representation (slider or buttons)
   - Metric definitions and guidance
   - All metrics required before submission

3. **Comment Management**
   - Optional comments for each metric
   - Overall comment field
   - Character limits with counters
   - Comments visible after evaluation period closes

4. **Score Visibility Control**
   - Hide other evaluators' scores during evaluation period
   - Reveal aggregated scores after period closes
   - Prevent bias from other evaluators
   - Clear indication of evaluation period status

5. **Evaluation Progress**
   - Track completion status
   - Show panel member progress
   - Identify behind-schedule evaluators
   - Send reminders for incomplete evaluations

### Data Entities
- Evaluation (id, ideaId, panelMemberId, feasibilityScore, impactScore, innovationScore, comments, createdAt)
- EvaluationComment (id, evaluationId, metricType, comment)
- EvaluationProgress (campaignId, totalIdeas, totalEvaluationsNeeded, completedEvaluations)

### APIs/Interfaces
- `GET /campaigns/{campaignId}/assigned-ideas` - Get assigned ideas
- `GET /ideas/{ideaId}/evaluation-form` - Get evaluation form
- `POST /evaluations` - Submit evaluation
- `PUT /evaluations/{evaluationId}` - Update evaluation
- `GET /evaluations/{ideaId}/{panelMemberId}` - Get specific evaluation
- `GET /ideas/{ideaId}/aggregated-scores` - Get aggregated scores (after period)
- `GET /campaigns/{campaignId}/evaluation-progress` - Get progress
- `GET /ideas/{ideaId}/can-evaluate` - Check if evaluation allowed

### Dependencies
- **Depends On**: Campaign Component (period validation), Idea Submission Unit (idea data), User Component (validation), Notification Component (notifications)
- **Depended On By**: Dashboard Unit, Leaderboard Unit, Analytics Unit, Recognition Unit
- **Integration Points**:
  - Campaign validation for evaluation period
  - Idea data from Submission Unit
  - User validation for panel members
  - Notifications for evaluation status

### Development Complexity
- **Complexity Level**: High
- **Estimated Effort**: 3-4 weeks
- **Team Size**: 3-4 developers
- **Key Challenges**: Score visibility control, evaluation period management, aggregation logic

### Testing Strategy
- Unit tests for scoring logic
- Integration tests with Campaign and Idea components
- Tests for score visibility during/after evaluation period
- End-to-end tests for complete evaluation workflow
- Test coverage target: 85%+

### Deployment Considerations
- Depends on Campaign Unit for period validation
- Depends on Submission Unit for idea data
- Database schema: evaluations, evaluation_comments tables
- Should be deployed after Campaign and Submission units

---

## Unit 3: Dashboards & Leaderboards

**Purpose**: Display real-time dashboards and leaderboards showing idea performance

**Scope**: Real-time dashboard, leaderboard ranking, and comparative analysis

### Components
- **Dashboard Component** (primary)
- **Leaderboard Component** (primary)
- **Evaluation Component** (shared - score data)
- **Idea Submission Component** (shared - idea data)
- **Campaign Component** (shared - campaign context)

### Services
- **Dashboard Service** - Orchestrates dashboard data aggregation

### User Stories Assigned
- Story 10: View Real-Time Dashboard with All Ideas
- Story 11: View Leaderboard Ranked by Composite Score
- Story 12: View Multi-Dimensional Comparative Analysis

### Key Features
1. **Real-Time Dashboard**
   - Display all ideas with current scores
   - Show composite score (average of three metrics)
   - Display evaluation progress per idea
   - Real-time updates within 5 seconds
   - Filtering by status, submitter, date range
   - Sorting by score, submission date, status
   - WebSocket connections for live updates

2. **Leaderboard**
   - Rank ideas by composite score
   - Display top 10, 20, 50, or all ideas
   - Show individual metric scores
   - Highlight user's own ideas
   - Sortable by rank, score, or individual metrics
   - Filterable by submitter or date range
   - Visual indicators for top 3 (badges)

3. **Comparative Analysis**
   - Compare ideas across metrics
   - Visual representations (radar chart, bar chart, table)
   - Distribution analysis
   - Percentile rankings
   - Side-by-side comparison
   - Mobile-responsive design

4. **Real-Time Updates**
   - WebSocket connections for bidirectional communication
   - Broadcast updates to all connected clients
   - Update propagation within 5 seconds
   - Efficient batch updates
   - Client-side caching

### Data Entities
- DashboardData (ideas[], totalCount, evaluationProgress, lastUpdated)
- IdeaWithScores (ideaId, title, submitter, scores, evaluationProgress, status)
- LeaderboardEntry (rank, ideaId, title, submitter, compositeScore, scores)
- ComparativeAnalysis (ideas[], metrics[], distributions[])

### APIs/Interfaces
- `GET /dashboard` - Get dashboard data
- `GET /ideas/{ideaId}/with-scores` - Get idea with scores
- `WS /dashboard/subscribe` - Subscribe to real-time updates
- `WS /dashboard/unsubscribe` - Unsubscribe from updates
- `GET /leaderboard` - Get leaderboard
- `GET /leaderboard/top/{count}` - Get top N ideas
- `GET /leaderboard/by-metric/{metric}` - Get ranking by metric
- `GET /comparative-analysis` - Get comparative analysis

### Dependencies
- **Depends On**: Evaluation Unit (score data), Submission Unit (idea data), Campaign Unit (campaign context)
- **Depended On By**: Recognition Unit (for badge display)
- **Integration Points**:
  - Real-time score updates from Evaluation Unit
  - Idea data from Submission Unit
  - Campaign context from Campaign Unit
  - Badge display from Recognition Unit

### Development Complexity
- **Complexity Level**: High
- **Estimated Effort**: 3-4 weeks
- **Team Size**: 3-4 developers
- **Key Challenges**: Real-time updates, WebSocket management, performance optimization, caching

### Testing Strategy
- Unit tests for dashboard logic
- Integration tests with Evaluation and Submission units
- WebSocket connection tests
- Real-time update tests
- Performance tests (dashboard loads in 2 seconds)
- End-to-end tests for complete dashboard workflow
- Test coverage target: 85%+

### Deployment Considerations
- Depends on Evaluation Unit for score data
- Depends on Submission Unit for idea data
- WebSocket infrastructure required
- Caching layer recommended
- Should be deployed after Evaluation and Submission units

---

## Unit 4: Analytics & Recognition

**Purpose**: Generate analytics insights and award recognition to top ideas

**Scope**: Analytics dashboards, reporting, recognition system, and badge awards

### Components
- **Analytics Component** (primary)
- **Recognition Component** (primary)
- **Evaluation Component** (shared - score data)
- **Idea Submission Component** (shared - idea/contributor data)
- **Campaign Component** (shared - campaign context)
- **Notification Component** (shared - notifications)
- **User Component** (shared - validation)

### Services
- **Analytics Service** - Orchestrates analytics and reporting
- **Recognition Service** - Orchestrates recognition workflow

### User Stories Assigned
- Story 13: View Analytics Dashboard with Top Ideas
- Story 14: View Comparative Analysis Across Evaluation Criteria
- Story 15: Generate Executive Report
- Story 16: Automatically Identify Top 3 Ideas
- Story 17: Award Digital Badges to Top 3 Ideas
- Story 18: Notify Winners of Recognition
- Story 19: Display Recognition Badges on User Profile
- Story 20: Display Recognition Badges on Leaderboard

### Key Features
1. **Analytics Dashboard**
   - Display top 10 ideas by score
   - Show key metrics (total ideas, avg score, completion %)
   - Trend analysis and distribution
   - Visual representations (charts, graphs)
   - Filterable by campaign, date range, submitter
   - Exportable data (CSV, PDF)

2. **Comparative Analysis**
   - Heatmap of ideas vs metrics
   - Distribution charts for each metric
   - Scatter plots showing metric relationships
   - Correlation analysis
   - Drill-down into specific ideas
   - Exportable analysis

3. **Executive Reporting**
   - Generate comprehensive reports
   - Executive summary with key metrics
   - Top ideas and trends
   - Visual representations
   - Export in PDF, Excel, PowerPoint
   - Scheduled report generation
   - ROI analysis (if implementation data available)

4. **Recognition System**
   - Automatic identification of top 3 ideas
   - Tie-breaking logic (Innovation, then Impact)
   - Manual override capability with justification
   - Digital badge creation and assignment
   - Badge display on profiles and leaderboard
   - Recognition history tracking

5. **Winner Notifications**
   - Email and in-app notifications
   - Congratulatory messages
   - Links to view badges and idea details
   - Shareable recognition
   - Notification logging

### Data Entities
- AnalyticsData (topIdeas[], distributions[], trends[], correlations[])
- Report (id, campaignId, type, format, generatedAt, data)
- Badge (id, ideaId, rank, awardedAt, awardedBy)
- Recognition (id, userId, badgeId, ideaId, awardedAt)
- RecognitionHistory (userId, badges[], totalRecognitions)

### APIs/Interfaces
- `GET /analytics/dashboard` - Get analytics dashboard
- `GET /analytics/top-ideas` - Get top ideas
- `GET /analytics/distribution` - Get distribution analysis
- `GET /analytics/trends` - Get trend analysis
- `GET /analytics/comparative` - Get comparative analysis
- `GET /analytics/correlation` - Get correlation analysis
- `POST /reports/generate` - Generate report
- `GET /reports/{reportId}` - Get report
- `POST /recognition/identify-top-3` - Identify top 3
- `POST /recognition/award-badges` - Award badges
- `POST /recognition/override` - Override top 3
- `GET /users/{userId}/badges` - Get user's badges
- `GET /users/{userId}/recognition-history` - Get recognition history

### Dependencies
- **Depends On**: Evaluation Unit (score data), Submission Unit (idea/contributor data), Campaign Unit (campaign context), Notification Component (notifications), User Component (validation)
- **Depended On By**: Dashboard Unit (for badge display)
- **Integration Points**:
  - Score data from Evaluation Unit
  - Idea and contributor data from Submission Unit
  - Campaign context from Campaign Unit
  - Notifications for winners
  - User validation for administrators

### Development Complexity
- **Complexity Level**: High
- **Estimated Effort**: 3-4 weeks
- **Team Size**: 3-4 developers
- **Key Challenges**: Analytics calculations, report generation, recognition workflow, notification coordination

### Testing Strategy
- Unit tests for analytics calculations
- Unit tests for recognition logic
- Integration tests with Evaluation and Submission units
- Report generation tests
- Notification tests
- End-to-end tests for complete analytics and recognition workflows
- Test coverage target: 85%+

### Deployment Considerations
- Depends on Evaluation Unit for score data
- Depends on Submission Unit for idea data
- Report generation may require background processing
- Should be deployed after Evaluation and Submission units

---

## Unit 5: Campaign Management

**Purpose**: Enable administrators to create and manage evaluation campaigns

**Scope**: Campaign creation, panel member assignment, and progress monitoring

### Components
- **Campaign Component** (primary)
- **User Component** (shared - validation)
- **Notification Component** (shared - notifications)

### Services
- **Campaign Service** - Orchestrates campaign management

### User Stories Assigned
- Story 21: Create and Configure Evaluation Campaign
- Story 22: Monitor Campaign Evaluation Progress

### Key Features
1. **Campaign Creation**
   - Create campaigns with name, description, dates
   - Configure evaluation period (start/end dates)
   - Validate date constraints
   - Save as draft or publish
   - Campaign status tracking (planning, active, evaluation, closed)

2. **Panel Member Assignment**
   - Assign panel members to campaigns
   - Select from employee list
   - Multiple panel members per campaign
   - Send notifications to assigned members
   - Track assignments

3. **Campaign Progress Monitoring**
   - View active campaigns
   - Display evaluation progress (% complete)
   - Show panel member status (completed, in progress, not started)
   - Identify behind-schedule evaluators
   - Send reminders to panel members
   - Close evaluation period manually

4. **Campaign Lifecycle**
   - Campaign status tracking
   - Evaluation period enforcement
   - Automatic score aggregation on period close
   - Trigger recognition workflow
   - Generate final analytics
   - Campaign closure

### Data Entities
- Campaign (id, name, description, startDate, endDate, evaluationStartDate, evaluationEndDate, status, createdBy, createdAt)
- CampaignPanelMember (campaignId, panelMemberId, assignedAt)
- CampaignStatus (campaignId, status, ideasCount, evaluationsCompleted, evaluationsNeeded)

### APIs/Interfaces
- `POST /campaigns` - Create campaign
- `GET /campaigns/{campaignId}` - Get campaign details
- `PUT /campaigns/{campaignId}` - Update campaign
- `DELETE /campaigns/{campaignId}` - Delete campaign
- `POST /campaigns/{campaignId}/panel-members` - Assign panel members
- `GET /campaigns/{campaignId}/panel-members` - Get assigned panel members
- `GET /campaigns/{campaignId}/status` - Get campaign status
- `GET /campaigns/{campaignId}/progress` - Get campaign progress
- `POST /campaigns/{campaignId}/close-evaluation-period` - Close evaluation period
- `POST /campaigns/{campaignId}/close` - Close campaign

### Dependencies
- **Depends On**: User Component (validation), Notification Component (notifications)
- **Depended On By**: Evaluation Unit (period validation), Submission Unit (campaign association), Dashboard Unit (campaign context), Analytics Unit (campaign context), Recognition Unit (campaign context)
- **Integration Points**:
  - User validation for administrators and panel members
  - Notifications for campaign and panel member updates
  - Campaign context provided to other units

### Development Complexity
- **Complexity Level**: Medium
- **Estimated Effort**: 2-3 weeks
- **Team Size**: 2-3 developers
- **Key Challenges**: Date validation, campaign lifecycle management, notification coordination

### Testing Strategy
- Unit tests for campaign logic
- Integration tests with User and Notification components
- Date validation tests
- Campaign lifecycle tests
- End-to-end tests for complete campaign workflow
- Test coverage target: 85%+

### Deployment Considerations
- Can be deployed independently
- Database schema: campaigns, campaign_panel_members tables
- Should be deployed before or alongside Evaluation Unit
- No external dependencies for core functionality

---

## Unit Development Sequence

### Recommended Development Order

**Phase 1: Foundation (Weeks 1-2)**
- **Unit 5: Campaign Management** - Foundation for campaign context
- **Unit 1: Idea Submission & Management** - Core submission workflow

**Phase 2: Evaluation (Weeks 3-4)**
- **Unit 2: Evaluation Framework** - Evaluation process and scoring

**Phase 3: Visualization (Weeks 5-6)**
- **Unit 3: Dashboards & Leaderboards** - Real-time dashboards
- **Unit 4: Analytics & Recognition** - Analytics and recognition (can start in parallel with Unit 3)

### Parallel Development Opportunities

**Can be developed in parallel:**
- Unit 1 (Submission) and Unit 5 (Campaign) - Independent
- Unit 3 (Dashboard) and Unit 4 (Analytics) - Both depend on Unit 2, can start together after Unit 2

**Must be sequential:**
- Unit 5 (Campaign) before Unit 2 (Evaluation) - Campaign provides period validation
- Unit 1 (Submission) before Unit 2 (Evaluation) - Evaluation needs ideas
- Unit 2 (Evaluation) before Unit 3 (Dashboard) - Dashboard needs scores
- Unit 2 (Evaluation) before Unit 4 (Analytics) - Analytics needs scores

### Critical Path
1. Unit 5: Campaign Management (foundation)
2. Unit 1: Idea Submission & Management (data)
3. Unit 2: Evaluation Framework (processing)
4. Unit 3 & 4: Dashboard/Analytics & Recognition (visualization)

---

## Shared Components Implementation

### User Component (Shared)
- Implement once, used by all units
- Provides authentication, authorization, user management
- Implement in Unit 1 or as separate shared component
- All units depend on this

### Notification Component (Shared)
- Implement once, used by all units
- Provides multi-channel notifications (in-app, email, SMS)
- Implement in Unit 1 or as separate shared component
- All units depend on this

### Campaign Component (Shared)
- Implement in Unit 5
- Provides campaign context and period validation
- Used by Units 2, 3, 4
- Unit 2 depends on this for period validation

---

## Integration Points

### Unit 1 ↔ Unit 2
- Unit 1 provides idea data to Unit 2
- Unit 2 retrieves ideas for evaluation
- API: `GET /ideas/{ideaId}`

### Unit 2 ↔ Unit 3
- Unit 2 provides score data to Unit 3
- Unit 3 retrieves scores for dashboard
- Real-time updates via WebSocket
- API: `GET /ideas/{ideaId}/aggregated-scores`

### Unit 2 ↔ Unit 4
- Unit 2 provides score data to Unit 4
- Unit 4 retrieves scores for analytics
- API: `GET /ideas/{ideaId}/aggregated-scores`

### Unit 3 ↔ Unit 4
- Unit 4 provides badge data to Unit 3
- Unit 3 displays badges on leaderboard
- API: `GET /ideas/{ideaId}/badges`

### Unit 5 ↔ All Units
- Unit 5 provides campaign context
- All units filter by campaign
- API: `GET /campaigns/{campaignId}`

---

## Summary

**5 Units of Work:**
1. Idea Submission & Management (2-3 weeks)
2. Evaluation Framework (3-4 weeks)
3. Dashboards & Leaderboards (3-4 weeks)
4. Analytics & Recognition (3-4 weeks)
5. Campaign Management (2-3 weeks)

**Total Estimated Effort**: 13-18 weeks (3.5-4.5 weeks with parallel development)

**Development Approach**: Hybrid parallel with dependency-based sequencing

**Deployment Strategy**: Independent deployment per unit with coordinated releases

**Key Success Factors**:
- Clear unit boundaries and interfaces
- Effective parallel development coordination
- Robust integration testing
- Real-time update performance
- Recognition workflow reliability
