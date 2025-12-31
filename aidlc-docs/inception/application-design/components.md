# Ideation Portal - Component Architecture

## Overview
The Ideation Portal uses a modular monolith architecture with clear module boundaries. This document defines the 8 core components, their responsibilities, and interfaces.

---

## Component 1: Idea Submission Component

**Purpose**: Handle idea creation, draft management, and contributor management

**Responsibilities**:
- Create new ideas with structured input fields
- Save ideas as drafts
- Retrieve and update draft ideas
- Add/remove contributors to ideas
- Validate idea data
- Manage idea metadata (timestamps, status)

**Key Interfaces**:
- `submitIdea(ideaData)` - Submit a new idea
- `saveDraft(ideaData)` - Save idea as draft
- `getDraft(draftId)` - Retrieve draft idea
- `updateDraft(draftId, ideaData)` - Update draft
- `deleteDraft(draftId)` - Delete draft
- `addContributor(ideaId, userId)` - Add contributor
- `removeContributor(ideaId, userId)` - Remove contributor
- `getIdea(ideaId)` - Retrieve submitted idea
- `getMyIdeas(userId)` - Get user's submitted ideas
- `validateIdeaData(ideaData)` - Validate idea input

**Data Entities**:
- Idea (id, title, description, expectedImpact, submitterId, contributors, status, createdAt, updatedAt)
- Draft (id, userId, ideaData, createdAt, updatedAt)
- Contributor (ideaId, userId, addedAt)

**Dependencies**:
- User Component (for user validation)
- Notification Component (for contributor notifications)

---

## Component 2: Evaluation Component

**Purpose**: Manage the evaluation process, scoring, and evaluation comments

**Responsibilities**:
- Create evaluation forms for assigned ideas
- Record evaluation scores (Feasibility, Impact, Innovation)
- Store evaluation comments and justifications
- Retrieve evaluations for ideas
- Calculate aggregated scores
- Manage evaluation status and progress
- Enforce evaluation period constraints

**Key Interfaces**:
- `getAssignedIdeas(panelMemberId, campaignId)` - Get ideas assigned to evaluator
- `getEvaluationForm(ideaId, panelMemberId)` - Get evaluation form
- `submitEvaluation(ideaId, panelMemberId, scores, comments)` - Submit evaluation
- `getEvaluation(ideaId, panelMemberId)` - Retrieve specific evaluation
- `getAggregatedScores(ideaId)` - Get aggregated scores (after period closes)
- `getEvaluationProgress(campaignId)` - Get evaluation completion status
- `canEvaluate(ideaId, panelMemberId, campaignId)` - Check if evaluation allowed
- `hideOtherEvaluations(ideaId, campaignId)` - Hide other evaluators' scores during period
- `revealAggregatedScores(campaignId)` - Reveal scores after period closes

**Data Entities**:
- Evaluation (id, ideaId, panelMemberId, feasibilityScore, impactScore, innovationScore, comments, createdAt)
- EvaluationComment (id, evaluationId, metricType, comment)
- EvaluationProgress (campaignId, totalIdeas, totalEvaluationsNeeded, completedEvaluations)

**Dependencies**:
- Campaign Component (for campaign/period validation)
- Idea Submission Component (for idea data)
- Notification Component (for evaluation notifications)

---

## Component 3: Dashboard Component

**Purpose**: Display real-time dashboard with all ideas and their current scores

**Responsibilities**:
- Aggregate idea data with current scores
- Provide real-time score updates
- Support filtering and sorting
- Calculate evaluation progress
- Manage dashboard state and caching
- Handle WebSocket connections for real-time updates

**Key Interfaces**:
- `getDashboardData(campaignId, filters)` - Get dashboard data with filters
- `getIdeaWithScores(ideaId)` - Get idea with current scores
- `subscribeToUpdates(campaignId, callback)` - Subscribe to real-time updates (WebSocket)
- `unsubscribeFromUpdates(subscriptionId)` - Unsubscribe from updates
- `getEvaluationProgress(campaignId)` - Get evaluation progress
- `sortIdeas(ideas, sortBy)` - Sort ideas by various criteria
- `filterIdeas(ideas, filters)` - Filter ideas by status, submitter, date
- `calculateCompositeScore(idea)` - Calculate average of three metrics

**Data Entities**:
- DashboardData (ideas[], totalCount, evaluationProgress, lastUpdated)
- IdeaWithScores (ideaId, title, submitter, scores, evaluationProgress, status)

**Dependencies**:
- Evaluation Component (for score data)
- Idea Submission Component (for idea data)
- Campaign Component (for campaign context)

---

## Component 4: Leaderboard Component

**Purpose**: Display ranked leaderboard of ideas by composite score

**Responsibilities**:
- Rank ideas by composite score
- Handle tie-breaking logic
- Provide multi-dimensional views
- Support filtering and sorting
- Manage leaderboard caching
- Highlight user's own ideas

**Key Interfaces**:
- `getLeaderboard(campaignId, limit, offset)` - Get ranked ideas
- `getTopIdeas(campaignId, count)` - Get top N ideas
- `getRankingByMetric(campaignId, metric)` - Get ranking by specific metric
- `getComparativeAnalysis(campaignId, ideaIds)` - Compare specific ideas
- `getUserRanking(campaignId, userId)` - Get user's idea ranking
- `calculateRank(ideaId, campaignId)` - Calculate rank for idea
- `resolveTies(ideas)` - Apply tie-breaking logic

**Data Entities**:
- LeaderboardEntry (rank, ideaId, title, submitter, compositeScore, feasibilityScore, impactScore, innovationScore)
- ComparativeAnalysis (ideas[], metrics[], distributions[])

**Dependencies**:
- Evaluation Component (for score data)
- Idea Submission Component (for idea data)

---

## Component 5: Analytics Component

**Purpose**: Generate analytics, insights, and reports

**Responsibilities**:
- Calculate analytics metrics
- Generate trend analysis
- Create comparative analysis
- Support data export
- Manage analytics caching
- Generate executive reports

**Key Interfaces**:
- `getAnalyticsDashboard(campaignId)` - Get analytics overview
- `getTopIdeas(campaignId, count)` - Get top performing ideas
- `getDistributionAnalysis(campaignId)` - Get score distribution
- `getTrendAnalysis(campaignId)` - Get trends over time
- `getComparativeAnalysis(campaignId)` - Compare metrics
- `getCorrelationAnalysis(campaignId)` - Analyze metric correlations
- `generateReport(campaignId, format)` - Generate report (PDF, Excel, CSV)
- `exportData(campaignId, format)` - Export analytics data
- `getHeatmap(campaignId)` - Get ideas vs metrics heatmap

**Data Entities**:
- AnalyticsData (topIdeas[], distributions[], trends[], correlations[])
- Report (id, campaignId, type, format, generatedAt, data)

**Dependencies**:
- Evaluation Component (for score data)
- Idea Submission Component (for idea data)
- Campaign Component (for campaign context)

---

## Component 6: Recognition Component

**Purpose**: Manage recognition badges and awards for top ideas

**Responsibilities**:
- Identify top 3 ideas
- Award digital badges
- Manage recognition history
- Display badges on profiles and leaderboard
- Handle manual overrides
- Manage badge metadata

**Key Interfaces**:
- `identifyTopIdeas(campaignId)` - Identify top 3 ideas
- `awardBadges(campaignId, ideaIds)` - Award badges to top ideas
- `overrideTopIdeas(campaignId, ideaIds, justification)` - Override top 3 selection
- `getBadges(userId)` - Get user's badges
- `getRecognitionHistory(userId)` - Get user's recognition history
- `displayBadgeOnProfile(userId, badgeId)` - Display badge on profile
- `displayBadgeOnLeaderboard(ideaId, badgeId)` - Display badge on leaderboard
- `revokeBadge(badgeId, reason)` - Revoke badge (if needed)

**Data Entities**:
- Badge (id, ideaId, rank, awardedAt, awardedBy)
- Recognition (id, userId, badgeId, ideaId, awardedAt)
- RecognitionHistory (userId, badges[], totalRecognitions)

**Dependencies**:
- Evaluation Component (for score data)
- Idea Submission Component (for idea/contributor data)
- Notification Component (for winner notifications)

---

## Component 7: Campaign Component

**Purpose**: Manage evaluation campaigns and cycles

**Responsibilities**:
- Create and configure campaigns
- Manage campaign dates and periods
- Assign panel members to campaigns
- Track campaign status
- Manage evaluation period constraints
- Monitor campaign progress

**Key Interfaces**:
- `createCampaign(campaignData)` - Create new campaign
- `getCampaign(campaignId)` - Get campaign details
- `updateCampaign(campaignId, campaignData)` - Update campaign
- `closeCampaign(campaignId)` - Close campaign
- `assignPanelMembers(campaignId, panelMemberIds)` - Assign evaluators
- `getAssignedPanelMembers(campaignId)` - Get assigned evaluators
- `getCampaignStatus(campaignId)` - Get campaign status
- `isEvaluationPeriodActive(campaignId)` - Check if evaluation period is active
- `closeEvaluationPeriod(campaignId)` - Close evaluation period
- `getCampaignProgress(campaignId)` - Get campaign progress

**Data Entities**:
- Campaign (id, name, description, startDate, endDate, evaluationStartDate, evaluationEndDate, status, createdBy, createdAt)
- CampaignPanelMember (campaignId, panelMemberId, assignedAt)
- CampaignStatus (campaignId, status, ideasCount, evaluationsCompleted, evaluationsNeeded)

**Dependencies**:
- User Component (for panel member validation)
- Notification Component (for campaign notifications)

---

## Component 8: User Component

**Purpose**: Manage users, authentication, and authorization

**Responsibilities**:
- User registration and authentication
- Role management (Employee, Panel Member, Administrator)
- User profile management
- Permission enforcement
- Session management
- Audit logging

**Key Interfaces**:
- `registerUser(userData)` - Register new user
- `authenticateUser(email, password)` - Authenticate user
- `getUserProfile(userId)` - Get user profile
- `updateUserProfile(userId, profileData)` - Update profile
- `assignRole(userId, role)` - Assign role to user
- `getUserRole(userId)` - Get user's role
- `hasPermission(userId, permission)` - Check user permission
- `createSession(userId)` - Create user session
- `validateSession(sessionToken)` - Validate session token
- `logoutUser(userId)` - Logout user
- `logAuditEvent(userId, action, details)` - Log audit event

**Data Entities**:
- User (id, email, password, name, role, createdAt, updatedAt)
- UserProfile (userId, submittedIdeas[], badges[], recognitions[])
- Session (id, userId, token, createdAt, expiresAt)
- AuditLog (id, userId, action, details, timestamp)

**Dependencies**:
- Notification Component (for user notifications)

---

## Component 9: Notification Component

**Purpose**: Handle multi-channel notifications (in-app, email, SMS)

**Responsibilities**:
- Send in-app notifications
- Send email notifications
- Send SMS notifications
- Manage notification preferences
- Track notification delivery
- Handle notification templates

**Key Interfaces**:
- `sendNotification(userId, notificationType, data)` - Send notification
- `sendInAppNotification(userId, message)` - Send in-app notification
- `sendEmailNotification(userId, subject, body)` - Send email
- `sendSMSNotification(userId, message)` - Send SMS
- `getNotifications(userId)` - Get user's notifications
- `markAsRead(notificationId)` - Mark notification as read
- `setNotificationPreferences(userId, preferences)` - Set user preferences
- `getNotificationTemplate(templateName)` - Get notification template

**Data Entities**:
- Notification (id, userId, type, message, read, createdAt)
- NotificationPreference (userId, inAppEnabled, emailEnabled, smsEnabled)
- NotificationTemplate (name, subject, body, variables[])

**Dependencies**:
- User Component (for user data)

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Ideation Portal Components                    │
└─────────────────────────────────────────────────────────────────┘

                          ┌──────────────┐
                          │ User         │
                          │ Component    │
                          └──────────────┘
                                 ▲
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │ Idea         │ │ Campaign     │ │ Notification │
            │ Submission   │ │ Component    │ │ Component    │
            │ Component    │ └──────────────┘ └──────────────┘
            └──────────────┘        ▲
                    ▲               │
                    │        ┌──────┴──────┐
                    │        ▼             ▼
                    │   ┌──────────────┐ ┌──────────────┐
                    │   │ Evaluation   │ │ Recognition  │
                    │   │ Component    │ │ Component    │
                    │   └──────────────┘ └──────────────┘
                    │        ▲
        ┌───────────┼────────┼───────────┐
        ▼           ▼        ▼           ▼
    ┌──────────┐ ┌──────────────┐ ┌──────────────┐
    │Dashboard │ │Leaderboard   │ │Analytics     │
    │Component │ │Component     │ │Component     │
    └──────────┘ └──────────────┘ └──────────────┘
```

---

## Component Responsibilities Summary

| Component | Primary Responsibility | Key Features |
|-----------|----------------------|--------------|
| Idea Submission | Manage idea creation and drafts | Submit, draft, contributors |
| Evaluation | Manage scoring and evaluation | Score, comments, progress |
| Dashboard | Real-time idea display | Filtering, sorting, real-time updates |
| Leaderboard | Rank ideas by score | Ranking, tie-breaking, comparison |
| Analytics | Generate insights and reports | Trends, distribution, export |
| Recognition | Award badges and recognition | Top 3 identification, badges |
| Campaign | Manage evaluation cycles | Campaign creation, panel assignment |
| User | Manage users and auth | Authentication, roles, permissions |
| Notification | Multi-channel notifications | In-app, email, SMS |

---

## Design Principles

1. **Modularity**: Each component has clear, single responsibility
2. **Loose Coupling**: Components communicate through well-defined interfaces
3. **High Cohesion**: Related functionality grouped within components
4. **Scalability**: Components can be scaled independently
5. **Testability**: Each component can be tested in isolation
6. **Maintainability**: Clear component boundaries and responsibilities
