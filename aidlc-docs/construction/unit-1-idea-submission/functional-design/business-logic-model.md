# Unit 1: Idea Submission & Management - Business Logic Model

## Overview
This document defines the detailed business logic, rules, and workflows for the Idea Submission & Management unit. It covers idea creation, draft management, contributor management, and all related business rules.

---

## Core Business Entities

### Idea Entity
```
Idea {
  id: UUID (primary key)
  title: String (required, max 200 chars)
  description: String (required, max 2000 chars)
  expectedImpact: Enum (High, Medium, Low)
  submitterId: UUID (foreign key to User)
  campaignId: UUID (foreign key to Campaign)
  status: Enum (Draft, Submitted, UnderEvaluation, Evaluated, Recognized)
  createdAt: DateTime
  updatedAt: DateTime
  submittedAt: DateTime (null until submitted)
  contributors: List<Contributor>
  documents: List<Document>
}
```

### Draft Entity
```
Draft {
  id: UUID (primary key)
  userId: UUID (foreign key to User)
  ideaData: JSON (partial idea data)
  createdAt: DateTime
  updatedAt: DateTime
  expiresAt: DateTime (30 days from creation)
}
```

### Contributor Entity
```
Contributor {
  id: UUID (primary key)
  ideaId: UUID (foreign key to Idea)
  userId: UUID (foreign key to User)
  addedAt: DateTime
  addedBy: UUID (foreign key to User - who added them)
}
```

### Document Entity
```
Document {
  id: UUID (primary key)
  ideaId: UUID (foreign key to Idea)
  fileName: String
  fileSize: Long
  fileType: String
  uploadedAt: DateTime
  uploadedBy: UUID (foreign key to User)
  storageUrl: String (cloud storage URL)
}
```

---

## Business Rules

### Idea Submission Rules

**BR1.1: Required Fields**
- Title is required (1-200 characters)
- Description is required (1-2000 characters)
- Expected Impact is required (High, Medium, Low)
- At least one of: title, description, or expected impact must be provided

**BR1.2: Idea Status Transitions**
```
Draft → Submitted → UnderEvaluation → Evaluated → Recognized (optional)
```
- Ideas start as Draft when saved without submission
- Ideas become Submitted when explicitly submitted
- Ideas become UnderEvaluation when evaluation period begins
- Ideas become Evaluated when evaluation period ends
- Ideas become Recognized if they win top 3

**BR1.3: Submission Validation**
- All required fields must be completed
- Title must be unique within campaign (no duplicate titles)
- Description must contain meaningful content (not just whitespace)
- Expected Impact must be one of: High, Medium, Low

**BR1.4: Campaign Association**
- Ideas must be associated with current active campaign
- Ideas cannot be submitted outside of campaign submission period
- Ideas submitted in one campaign cannot be moved to another

**BR1.5: Submitter Validation**
- Only authenticated employees can submit ideas
- Submitter must have Employee or higher role
- Submitter must be active user (not deactivated)

### Draft Management Rules

**BR2.1: Draft Creation**
- Drafts are created when user clicks "Save as Draft"
- Drafts can contain partial idea data
- Drafts are associated with the user who created them
- Drafts are retained for 30 days from last update

**BR2.2: Draft Expiration**
- Drafts automatically expire after 30 days of inactivity
- Expired drafts are soft-deleted (marked as deleted, not removed)
- Users are notified before draft expiration (optional)
- Expired drafts can be permanently deleted after 90 days

**BR2.3: Draft to Submission**
- Drafts can be converted to submitted ideas
- All required fields must be completed before submission
- Draft data is copied to new Idea entity
- Original draft is marked as converted

**BR2.4: Draft Editing**
- Only the draft owner can edit their draft
- Draft can be edited multiple times
- Each edit updates the updatedAt timestamp
- Draft data is validated on each save (partial validation)

**BR2.5: Draft Deletion**
- Only the draft owner can delete their draft
- Deletion requires confirmation
- Deleted drafts are soft-deleted (marked as deleted)
- Soft-deleted drafts can be permanently deleted after 30 days

### Contributor Management Rules

**BR3.1: Adding Contributors**
- Only the idea submitter can add contributors
- Contributors must be valid employees (active users)
- Contributors cannot be added after idea is submitted (optional - can be changed)
- Same user cannot be added as contributor twice
- Submitter cannot add themselves as contributor

**BR3.2: Contributor Notifications**
- When contributor is added, they receive notification
- Notification includes idea title and link to view idea
- Notification is sent via email and in-app
- Contributor can view the shared idea immediately

**BR3.3: Contributor Permissions**
- Contributors can view the shared idea
- Contributors can edit the shared idea (title, description, documents)
- Contributors cannot remove other contributors
- Contributors cannot delete the idea
- Contributors receive recognition if idea wins

**BR3.4: Removing Contributors**
- Only the idea submitter can remove contributors
- Removal requires confirmation
- Removed contributor loses access to edit the idea
- Removed contributor still receives recognition if idea was already recognized

**BR3.5: Contributor Limits**
- Maximum 10 contributors per idea (configurable)
- Submitter + contributors = total team size
- If limit reached, must remove contributor before adding new one

### Idea Viewing Rules

**BR4.1: Visibility**
- Submitted ideas are visible to all employees
- Draft ideas are visible only to owner and contributors
- Ideas are filtered by campaign
- Ideas show current status to all viewers

**BR4.2: Idea Details Display**
- Title, description, expected impact always shown
- Submitter name always shown
- Contributors list always shown
- Documents list always shown
- Submission date always shown
- Evaluation scores shown only after evaluation period closes

**BR4.3: Idea Editing**
- Only submitter can edit submitted ideas
- Editing allowed only before evaluation period begins
- Contributors can edit if submitter allows (configurable)
- Editing updates the updatedAt timestamp
- Edit history is maintained (optional)

**BR4.4: Idea Deletion**
- Only submitter can delete submitted ideas
- Deletion allowed only before evaluation period begins
- Deletion requires confirmation
- Deleted ideas are soft-deleted (marked as deleted)
- Soft-deleted ideas can be permanently deleted after 30 days

---

## Workflows

### Workflow 1: Submit New Idea

```
1. User clicks "Submit New Idea"
2. System displays idea submission form
3. User fills in required fields:
   - Title (1-200 chars)
   - Description (1-2000 chars)
   - Expected Impact (High/Medium/Low)
   - Optional: Documents, Contributors
4. User clicks "Submit"
5. System validates all required fields
6. System validates title uniqueness within campaign
7. System validates submitter is active employee
8. System validates campaign submission period is active
9. System creates Idea entity with status=Submitted
10. System associates idea with current campaign
11. System associates idea with submitter
12. System adds contributors if provided
13. System sends notifications to contributors
14. System logs audit event
15. System returns confirmation with idea ID
16. User is redirected to idea detail view
```

### Workflow 2: Save Idea as Draft

```
1. User fills in idea form (partial or complete)
2. User clicks "Save as Draft"
3. System validates submitter is authenticated
4. System validates campaign is active
5. System creates or updates Draft entity
6. System stores partial idea data in draft
7. System sets draft expiration to 30 days from now
8. System logs audit event
9. System returns confirmation
10. User can continue editing or leave
```

### Workflow 3: Resume Editing Draft

```
1. User navigates to "My Ideas" or "My Drafts"
2. System displays list of user's drafts
3. User clicks on draft to edit
4. System retrieves draft data
5. System validates draft has not expired
6. System displays form pre-populated with draft data
7. User edits data
8. User clicks "Save as Draft" or "Submit"
9. If "Save as Draft": Update draft (Workflow 2)
10. If "Submit": Convert draft to submitted idea (Workflow 4)
```

### Workflow 4: Convert Draft to Submitted Idea

```
1. User editing draft clicks "Submit"
2. System validates all required fields are completed
3. System validates title uniqueness within campaign
4. System validates submitter is active employee
5. System validates campaign submission period is active
6. System creates Idea entity from draft data
7. System sets idea status to Submitted
8. System associates idea with current campaign
9. System associates idea with submitter
10. System adds contributors from draft if any
11. System sends notifications to contributors
12. System marks draft as converted
13. System logs audit event
14. System returns confirmation with idea ID
15. User is redirected to idea detail view
```

### Workflow 5: Add Contributor to Idea

```
1. Idea submitter clicks "Add Contributor"
2. System displays contributor selection dialog
3. System displays searchable list of employees
4. Submitter searches for colleague
5. Submitter selects colleague from list
6. System validates:
   - Colleague is active employee
   - Colleague is not already contributor
   - Colleague is not submitter
   - Contributor limit not reached
7. System adds Contributor entity
8. System sends notification to contributor
9. System logs audit event
10. System returns confirmation
11. Contributor list is updated
```

### Workflow 6: View My Submitted Ideas

```
1. User navigates to "My Ideas"
2. System retrieves all ideas submitted by user
3. System retrieves all ideas where user is contributor
4. System combines and deduplicates lists
5. System displays ideas with:
   - Title, Submitter, Submission Date, Status
   - Evaluation Progress (if under evaluation)
   - Scores (if evaluated)
   - Recognition badge (if recognized)
6. System allows filtering by status
7. System allows sorting by date, status, score
8. User can click on idea to view details
```

### Workflow 7: Edit Submitted Idea

```
1. Idea submitter views submitted idea
2. System checks if editing is allowed:
   - Idea status is Submitted (not UnderEvaluation or later)
   - Evaluation period has not started
3. If allowed, system displays "Edit" button
4. Submitter clicks "Edit"
5. System displays form pre-populated with idea data
6. Submitter edits data
7. System validates all required fields
8. System validates title uniqueness (excluding current idea)
9. Submitter clicks "Save"
10. System updates Idea entity
11. System updates updatedAt timestamp
12. System logs audit event
13. System returns confirmation
14. User is redirected to idea detail view
```

---

## Data Validation Rules

### Title Validation
- Required: Yes
- Min length: 1 character
- Max length: 200 characters
- Allowed characters: Alphanumeric, spaces, punctuation
- Trimmed: Yes (leading/trailing whitespace removed)
- Unique: Yes (within campaign)

### Description Validation
- Required: Yes
- Min length: 1 character
- Max length: 2000 characters
- Allowed characters: Alphanumeric, spaces, punctuation, newlines
- Trimmed: Yes (leading/trailing whitespace removed)
- Not just whitespace: Yes (must contain meaningful content)

### Expected Impact Validation
- Required: Yes
- Allowed values: High, Medium, Low
- Case-insensitive: Yes
- Default: None (must be explicitly selected)

### Document Validation
- File size: Max 10 MB per file
- File types: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, PNG, JPG, JPEG
- Max files per idea: 5
- Virus scan: Yes (before storage)
- Storage: Cloud storage (S3, Azure Blob, etc.)

---

## Error Handling

### Validation Errors
- Return 400 Bad Request with detailed error messages
- Include field name and validation rule that failed
- Provide suggestions for correction

### Authorization Errors
- Return 403 Forbidden if user lacks permission
- Include reason for denial

### Not Found Errors
- Return 404 Not Found if idea/draft not found
- Include resource type and ID

### Conflict Errors
- Return 409 Conflict if title already exists
- Return 409 Conflict if draft already converted
- Include details of conflict

### Server Errors
- Return 500 Internal Server Error for unexpected errors
- Log error details for debugging
- Return generic error message to user

---

## Performance Considerations

### Database Optimization
- Index on userId for draft retrieval
- Index on campaignId for idea filtering
- Index on status for status-based queries
- Index on submitterId for user's ideas
- Composite index on (campaignId, status) for filtering

### Caching Strategy
- Cache user's ideas list (5-minute TTL)
- Cache draft list (1-minute TTL)
- Invalidate cache on create/update/delete
- Cache contributor list per idea (1-hour TTL)

### Query Optimization
- Use pagination for large result sets (default 20 per page)
- Lazy load contributors and documents
- Use database projections to fetch only needed fields
- Batch fetch related data to reduce N+1 queries

---

## Audit & Logging

### Events to Log
- Idea submitted
- Draft created
- Draft updated
- Draft deleted
- Draft converted to idea
- Contributor added
- Contributor removed
- Idea edited
- Idea deleted
- Idea viewed (optional)

### Audit Log Fields
- Event type
- User ID
- Idea ID / Draft ID
- Timestamp
- Changes made (for updates)
- IP address
- User agent

---

## Summary

The Idea Submission & Management unit implements:
- **Idea Submission**: Create and submit ideas with validation
- **Draft Management**: Save, edit, and convert drafts
- **Contributor Management**: Add colleagues to ideas
- **Idea Viewing**: View submitted ideas with filtering and sorting
- **Idea Editing**: Edit ideas before evaluation begins
- **Validation**: Comprehensive validation of all inputs
- **Error Handling**: Detailed error messages and logging
- **Performance**: Optimized queries and caching
- **Audit**: Complete audit trail of all operations
