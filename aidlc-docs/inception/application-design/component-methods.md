# Ideation Portal - Component Methods

## Overview
This document defines the method signatures for each component. Detailed business logic and implementation rules will be defined in the Functional Design phase (per-unit, CONSTRUCTION phase).

---

## Idea Submission Component Methods

### Submission Methods

```python
def submitIdea(
    userId: str,
    title: str,
    description: str,
    expectedImpact: str,
    documents: List[File] = None,
    contributors: List[str] = None
) -> IdeaResponse:
    """
    Submit a new idea for evaluation.
    
    Returns: Submitted idea with ID and confirmation
    """
    pass

def saveDraft(
    userId: str,
    draftId: str = None,
    title: str = None,
    description: str = None,
    expectedImpact: str = None,
    documents: List[File] = None
) -> DraftResponse:
    """
    Save idea as draft for later completion.
    
    Returns: Draft with ID and save confirmation
    """
    pass

def getDraft(
    userId: str,
    draftId: str
) -> DraftData:
    """
    Retrieve a draft idea for editing.
    
    Returns: Draft data with all fields
    """
    pass

def updateDraft(
    userId: str,
    draftId: str,
    ideaData: IdeaData
) -> DraftResponse:
    """
    Update an existing draft.
    
    Returns: Updated draft confirmation
    """
    pass

def deleteDraft(
    userId: str,
    draftId: str
) -> ConfirmationResponse:
    """
    Delete a draft idea.
    
    Returns: Deletion confirmation
    """
    pass
```

### Contributor Methods

```python
def addContributor(
    ideaId: str,
    userId: str,
    contributorUserId: str
) -> ContributorResponse:
    """
    Add a contributor to an idea.
    
    Returns: Updated contributor list
    """
    pass

def removeContributor(
    ideaId: str,
    userId: str,
    contributorUserId: str
) -> ContributorResponse:
    """
    Remove a contributor from an idea.
    
    Returns: Updated contributor list
    """
    pass

def getContributors(
    ideaId: str
) -> List[ContributorData]:
    """
    Get all contributors for an idea.
    
    Returns: List of contributors
    """
    pass
```

### Retrieval Methods

```python
def getIdea(
    ideaId: str,
    userId: str = None
) -> IdeaData:
    """
    Retrieve a submitted idea.
    
    Returns: Complete idea data
    """
    pass

def getMyIdeas(
    userId: str,
    status: str = None,
    sortBy: str = None
) -> List[IdeaData]:
    """
    Get all ideas submitted by user.
    
    Returns: List of user's ideas
    """
    pass

def getIdeasByStatus(
    status: str,
    campaignId: str = None
) -> List[IdeaData]:
    """
    Get ideas filtered by status.
    
    Returns: List of ideas with specified status
    """
    pass
```

### Validation Methods

```python
def validateIdeaData(
    ideaData: IdeaData
) -> ValidationResult:
    """
    Validate idea input data.
    
    Returns: Validation result with errors if any
    """
    pass

def validateTitle(
    title: str
) -> ValidationResult:
    """
    Validate idea title.
    
    Returns: Validation result
    """
    pass

def validateDescription(
    description: str
) -> ValidationResult:
    """
    Validate idea description.
    
    Returns: Validation result
    """
    pass
```

---

## Evaluation Component Methods

### Evaluation Submission Methods

```python
def submitEvaluation(
    ideaId: str,
    panelMemberId: str,
    campaignId: str,
    feasibilityScore: int,
    impactScore: int,
    innovationScore: int,
    comments: Dict[str, str] = None,
    overallComment: str = None
) -> EvaluationResponse:
    """
    Submit evaluation scores for an idea.
    
    Returns: Evaluation confirmation with ID
    """
    pass

def updateEvaluation(
    evaluationId: str,
    panelMemberId: str,
    scores: Dict[str, int],
    comments: Dict[str, str] = None
) -> EvaluationResponse:
    """
    Update an existing evaluation.
    
    Returns: Updated evaluation confirmation
    """
    pass
```

### Retrieval Methods

```python
def getAssignedIdeas(
    panelMemberId: str,
    campaignId: str,
    status: str = None
) -> List[IdeaForEvaluation]:
    """
    Get ideas assigned to panel member for evaluation.
    
    Returns: List of assigned ideas
    """
    pass

def getEvaluationForm(
    ideaId: str,
    panelMemberId: str
) -> EvaluationForm:
    """
    Get evaluation form for an idea.
    
    Returns: Form with idea details and scoring interface
    """
    pass

def getEvaluation(
    ideaId: str,
    panelMemberId: str
) -> EvaluationData:
    """
    Retrieve a specific evaluation.
    
    Returns: Evaluation data with scores and comments
    """
    pass

def getEvaluationsByIdea(
    ideaId: str,
    includeHidden: bool = False
) -> List[EvaluationData]:
    """
    Get all evaluations for an idea.
    
    Returns: List of evaluations (hidden if period active)
    """
    pass
```

### Score Aggregation Methods

```python
def getAggregatedScores(
    ideaId: str
) -> AggregatedScores:
    """
    Get aggregated scores for an idea.
    
    Returns: Average scores for each metric
    """
    pass

def calculateCompositeScore(
    ideaId: str
) -> float:
    """
    Calculate composite score (average of three metrics).
    
    Returns: Composite score
    """
    pass

def getScoreDistribution(
    campaignId: str
) -> ScoreDistribution:
    """
    Get distribution of scores across all ideas.
    
    Returns: Distribution data for analytics
    """
    pass
```

### Progress and Status Methods

```python
def getEvaluationProgress(
    campaignId: str
) -> EvaluationProgress:
    """
    Get evaluation completion progress for campaign.
    
    Returns: Progress data (completed, total, percentage)
    """
    pass

def getPanelMemberProgress(
    campaignId: str,
    panelMemberId: str
) -> PanelMemberProgress:
    """
    Get evaluation progress for specific panel member.
    
    Returns: Progress data for panel member
    """
    pass

def canEvaluate(
    ideaId: str,
    panelMemberId: str,
    campaignId: str
) -> bool:
    """
    Check if evaluation is allowed for idea.
    
    Returns: True if evaluation allowed, False otherwise
    """
    pass
```

### Visibility Control Methods

```python
def hideOtherEvaluations(
    ideaId: str,
    campaignId: str
) -> ConfirmationResponse:
    """
    Hide other evaluators' scores during evaluation period.
    
    Returns: Confirmation
    """
    pass

def revealAggregatedScores(
    campaignId: str
) -> ConfirmationResponse:
    """
    Reveal aggregated scores after evaluation period closes.
    
    Returns: Confirmation
    """
    pass

def canViewOtherScores(
    ideaId: str,
    campaignId: str
) -> bool:
    """
    Check if other evaluators' scores are visible.
    
    Returns: True if visible, False otherwise
    """
    pass
```

---

## Dashboard Component Methods

```python
def getDashboardData(
    campaignId: str,
    filters: DashboardFilters = None,
    sortBy: str = None
) -> DashboardData:
    """
    Get dashboard data with all ideas and current scores.
    
    Returns: Dashboard data with ideas, scores, progress
    """
    pass

def getIdeaWithScores(
    ideaId: str
) -> IdeaWithScores:
    """
    Get idea with current aggregated scores.
    
    Returns: Idea data with scores
    """
    pass

def subscribeToUpdates(
    campaignId: str,
    userId: str,
    callback: Callable
) -> SubscriptionId:
    """
    Subscribe to real-time dashboard updates via WebSocket.
    
    Returns: Subscription ID for later unsubscribe
    """
    pass

def unsubscribeFromUpdates(
    subscriptionId: str
) -> ConfirmationResponse:
    """
    Unsubscribe from real-time updates.
    
    Returns: Confirmation
    """
    pass

def sortIdeas(
    ideas: List[IdeaData],
    sortBy: str,
    order: str = "desc"
) -> List[IdeaData]:
    """
    Sort ideas by specified criteria.
    
    Returns: Sorted ideas
    """
    pass

def filterIdeas(
    ideas: List[IdeaData],
    filters: DashboardFilters
) -> List[IdeaData]:
    """
    Filter ideas by specified criteria.
    
    Returns: Filtered ideas
    """
    pass
```

---

## Leaderboard Component Methods

```python
def getLeaderboard(
    campaignId: str,
    limit: int = 10,
    offset: int = 0
) -> LeaderboardData:
    """
    Get ranked leaderboard of ideas.
    
    Returns: Ranked ideas with scores
    """
    pass

def getTopIdeas(
    campaignId: str,
    count: int = 10
) -> List[LeaderboardEntry]:
    """
    Get top N ideas by composite score.
    
    Returns: Top ideas
    """
    pass

def getRankingByMetric(
    campaignId: str,
    metric: str,
    limit: int = 10
) -> List[LeaderboardEntry]:
    """
    Get ranking by specific metric (Feasibility, Impact, Innovation).
    
    Returns: Ideas ranked by metric
    """
    pass

def getComparativeAnalysis(
    campaignId: str,
    ideaIds: List[str]
) -> ComparativeAnalysis:
    """
    Compare specific ideas across metrics.
    
    Returns: Comparative analysis data
    """
    pass

def getUserRanking(
    campaignId: str,
    userId: str
) -> UserRankingData:
    """
    Get ranking of user's ideas.
    
    Returns: User's ideas with rankings
    """
    pass

def calculateRank(
    ideaId: str,
    campaignId: str
) -> int:
    """
    Calculate rank for specific idea.
    
    Returns: Rank number
    """
    pass
```

---

## Analytics Component Methods

```python
def getAnalyticsDashboard(
    campaignId: str
) -> AnalyticsDashboard:
    """
    Get analytics overview dashboard.
    
    Returns: Analytics data with key metrics
    """
    pass

def getTopIdeas(
    campaignId: str,
    count: int = 10
) -> List[TopIdeaData]:
    """
    Get top performing ideas.
    
    Returns: Top ideas with scores
    """
    pass

def getDistributionAnalysis(
    campaignId: str
) -> DistributionAnalysis:
    """
    Get score distribution analysis.
    
    Returns: Distribution data for each metric
    """
    pass

def getTrendAnalysis(
    campaignId: str,
    previousCampaignId: str = None
) -> TrendAnalysis:
    """
    Get trend analysis over time.
    
    Returns: Trend data
    """
    pass

def getComparativeAnalysis(
    campaignId: str
) -> ComparativeAnalysis:
    """
    Get comparative analysis across metrics.
    
    Returns: Comparative analysis data
    """
    pass

def getCorrelationAnalysis(
    campaignId: str
) -> CorrelationAnalysis:
    """
    Get correlation analysis between metrics.
    
    Returns: Correlation data
    """
    pass

def generateReport(
    campaignId: str,
    reportType: str,
    format: str = "pdf"
) -> Report:
    """
    Generate executive report.
    
    Returns: Report in specified format
    """
    pass

def exportData(
    campaignId: str,
    format: str = "csv"
) -> ExportedData:
    """
    Export analytics data.
    
    Returns: Data in specified format
    """
    pass

def getHeatmap(
    campaignId: str
) -> HeatmapData:
    """
    Get heatmap of ideas vs metrics.
    
    Returns: Heatmap data
    """
    pass
```

---

## Recognition Component Methods

```python
def identifyTopIdeas(
    campaignId: str
) -> TopIdeasData:
    """
    Identify top 3 ideas by composite score.
    
    Returns: Top 3 ideas with scores
    """
    pass

def awardBadges(
    campaignId: str,
    ideaIds: List[str]
) -> BadgeAwardResponse:
    """
    Award digital badges to top ideas.
    
    Returns: Confirmation with badge details
    """
    pass

def overrideTopIdeas(
    campaignId: str,
    ideaIds: List[str],
    justification: str
) -> OverrideResponse:
    """
    Override automatic top 3 selection.
    
    Returns: Confirmation with override details
    """
    pass

def getBadges(
    userId: str
) -> List[BadgeData]:
    """
    Get user's earned badges.
    
    Returns: List of badges
    """
    pass

def getRecognitionHistory(
    userId: str
) -> RecognitionHistory:
    """
    Get user's recognition history.
    
    Returns: History of recognitions
    """
    pass

def displayBadgeOnProfile(
    userId: str,
    badgeId: str
) -> ConfirmationResponse:
    """
    Display badge on user profile.
    
    Returns: Confirmation
    """
    pass

def displayBadgeOnLeaderboard(
    ideaId: str,
    badgeId: str
) -> ConfirmationResponse:
    """
    Display badge on leaderboard.
    
    Returns: Confirmation
    """
    pass
```

---

## Campaign Component Methods

```python
def createCampaign(
    name: str,
    description: str,
    startDate: datetime,
    endDate: datetime,
    evaluationStartDate: datetime,
    evaluationEndDate: datetime,
    createdBy: str
) -> CampaignResponse:
    """
    Create new evaluation campaign.
    
    Returns: Campaign with ID
    """
    pass

def getCampaign(
    campaignId: str
) -> CampaignData:
    """
    Get campaign details.
    
    Returns: Campaign data
    """
    pass

def updateCampaign(
    campaignId: str,
    campaignData: CampaignData
) -> CampaignResponse:
    """
    Update campaign details.
    
    Returns: Updated campaign confirmation
    """
    pass

def closeCampaign(
    campaignId: str
) -> ConfirmationResponse:
    """
    Close campaign.
    
    Returns: Confirmation
    """
    pass

def assignPanelMembers(
    campaignId: str,
    panelMemberIds: List[str]
) -> AssignmentResponse:
    """
    Assign panel members to campaign.
    
    Returns: Assignment confirmation
    """
    pass

def getAssignedPanelMembers(
    campaignId: str
) -> List[PanelMemberData]:
    """
    Get panel members assigned to campaign.
    
    Returns: List of panel members
    """
    pass

def getCampaignStatus(
    campaignId: str
) -> CampaignStatus:
    """
    Get campaign status.
    
    Returns: Status data
    """
    pass

def isEvaluationPeriodActive(
    campaignId: str
) -> bool:
    """
    Check if evaluation period is active.
    
    Returns: True if active, False otherwise
    """
    pass

def closeEvaluationPeriod(
    campaignId: str
) -> ConfirmationResponse:
    """
    Close evaluation period.
    
    Returns: Confirmation
    """
    pass

def getCampaignProgress(
    campaignId: str
) -> CampaignProgress:
    """
    Get campaign progress.
    
    Returns: Progress data
    """
    pass
```

---

## User Component Methods

```python
def registerUser(
    email: str,
    password: str,
    name: str,
    role: str
) -> UserResponse:
    """
    Register new user.
    
    Returns: User with ID
    """
    pass

def authenticateUser(
    email: str,
    password: str
) -> AuthenticationResponse:
    """
    Authenticate user.
    
    Returns: Session token if successful
    """
    pass

def getUserProfile(
    userId: str
) -> UserProfile:
    """
    Get user profile.
    
    Returns: User profile data
    """
    pass

def updateUserProfile(
    userId: str,
    profileData: UserProfile
) -> UserResponse:
    """
    Update user profile.
    
    Returns: Updated profile confirmation
    """
    pass

def assignRole(
    userId: str,
    role: str,
    assignedBy: str
) -> RoleAssignmentResponse:
    """
    Assign role to user.
    
    Returns: Assignment confirmation
    """
    pass

def getUserRole(
    userId: str
) -> str:
    """
    Get user's role.
    
    Returns: Role string
    """
    pass

def hasPermission(
    userId: str,
    permission: str
) -> bool:
    """
    Check if user has permission.
    
    Returns: True if permitted, False otherwise
    """
    pass

def createSession(
    userId: str
) -> SessionResponse:
    """
    Create user session.
    
    Returns: Session token
    """
    pass

def validateSession(
    sessionToken: str
) -> SessionValidation:
    """
    Validate session token.
    
    Returns: Validation result with user ID if valid
    """
    pass

def logoutUser(
    userId: str
) -> ConfirmationResponse:
    """
    Logout user.
    
    Returns: Confirmation
    """
    pass

def logAuditEvent(
    userId: str,
    action: str,
    details: Dict
) -> AuditLogResponse:
    """
    Log audit event.
    
    Returns: Log confirmation
    """
    pass
```

---

## Notification Component Methods

```python
def sendNotification(
    userId: str,
    notificationType: str,
    data: Dict
) -> NotificationResponse:
    """
    Send notification to user.
    
    Returns: Notification confirmation
    """
    pass

def sendInAppNotification(
    userId: str,
    message: str,
    actionUrl: str = None
) -> NotificationResponse:
    """
    Send in-app notification.
    
    Returns: Notification confirmation
    """
    pass

def sendEmailNotification(
    userId: str,
    subject: str,
    body: str,
    templateName: str = None
) -> NotificationResponse:
    """
    Send email notification.
    
    Returns: Notification confirmation
    """
    pass

def sendSMSNotification(
    userId: str,
    message: str
) -> NotificationResponse:
    """
    Send SMS notification.
    
    Returns: Notification confirmation
    """
    pass

def getNotifications(
    userId: str,
    limit: int = 20,
    offset: int = 0
) -> List[NotificationData]:
    """
    Get user's notifications.
    
    Returns: List of notifications
    """
    pass

def markAsRead(
    notificationId: str
) -> ConfirmationResponse:
    """
    Mark notification as read.
    
    Returns: Confirmation
    """
    pass

def setNotificationPreferences(
    userId: str,
    preferences: NotificationPreferences
) -> PreferencesResponse:
    """
    Set user's notification preferences.
    
    Returns: Preferences confirmation
    """
    pass

def getNotificationTemplate(
    templateName: str
) -> NotificationTemplate:
    """
    Get notification template.
    
    Returns: Template data
    """
    pass
```

---

## Notes

- All method signatures are high-level and will be refined during Functional Design phase
- Detailed business logic and validation rules will be defined per-unit in CONSTRUCTION phase
- Error handling and exception types will be defined in Functional Design
- Database schema and data persistence will be defined in Infrastructure Design
- API endpoint mappings will be defined in Code Generation phase
