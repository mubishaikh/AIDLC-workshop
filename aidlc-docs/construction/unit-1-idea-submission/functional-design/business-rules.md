# Unit 1: Idea Submission & Management - Business Rules

## Overview
This document consolidates all business rules for the Idea Submission & Management unit in a structured format for easy reference during implementation.

---

## Rule Categories

### Category 1: Idea Submission Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR1.1 | Title required, 1-200 chars | Form validation + DB constraint | Prevents invalid submissions |
| BR1.2 | Description required, 1-2000 chars | Form validation + DB constraint | Ensures meaningful ideas |
| BR1.3 | Expected Impact required (High/Medium/Low) | Form validation + DB constraint | Enables impact assessment |
| BR1.4 | Title must be unique within campaign | DB unique constraint | Prevents duplicate ideas |
| BR1.5 | Description must not be whitespace only | Form validation | Ensures meaningful content |
| BR1.6 | Only authenticated employees can submit | Authentication check | Ensures accountability |
| BR1.7 | Submitter must have Employee+ role | Authorization check | Restricts to employees |
| BR1.8 | Submitter must be active user | User status check | Prevents inactive users |
| BR1.9 | Campaign submission period must be active | Campaign period check | Enforces submission window |
| BR1.10 | Idea must be associated with current campaign | Auto-association | Ensures campaign tracking |

### Category 2: Draft Management Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR2.1 | Drafts can contain partial data | No validation on save | Allows incremental work |
| BR2.2 | Drafts expire after 30 days | Scheduled job | Prevents stale drafts |
| BR2.3 | Only draft owner can edit | Authorization check | Ensures privacy |
| BR2.4 | Only draft owner can delete | Authorization check | Ensures privacy |
| BR2.5 | Draft deletion requires confirmation | UI confirmation | Prevents accidental deletion |
| BR2.6 | Expired drafts soft-deleted | Soft delete flag | Allows recovery |
| BR2.7 | Soft-deleted drafts permanently deleted after 90 days | Scheduled job | Cleanup old data |
| BR2.8 | Draft conversion requires all required fields | Validation on submit | Ensures complete ideas |
| BR2.9 | Draft title must be unique (if provided) | DB unique constraint | Prevents duplicates |
| BR2.10 | Draft can be converted only once | Status check | Prevents duplicate ideas |

### Category 3: Contributor Management Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR3.1 | Only submitter can add contributors | Authorization check | Ensures control |
| BR3.2 | Contributors must be active employees | User status check | Ensures valid users |
| BR3.3 | Same user cannot be added twice | Uniqueness check | Prevents duplicates |
| BR3.4 | Submitter cannot add themselves | Self-check | Prevents self-contribution |
| BR3.5 | Max 10 contributors per idea | Count check | Prevents abuse |
| BR3.6 | Contributor added notification sent | Event trigger | Ensures awareness |
| BR3.7 | Contributors can view shared idea | Permission grant | Enables collaboration |
| BR3.8 | Contributors can edit shared idea | Permission grant | Enables collaboration |
| BR3.9 | Contributors cannot remove other contributors | Authorization check | Prevents unauthorized removal |
| BR3.10 | Contributors cannot delete idea | Authorization check | Prevents unauthorized deletion |
| BR3.11 | Contributors receive recognition if idea wins | Recognition logic | Ensures fair credit |
| BR3.12 | Only submitter can remove contributors | Authorization check | Ensures control |
| BR3.13 | Contributor removal requires confirmation | UI confirmation | Prevents accidental removal |

### Category 4: Idea Viewing Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR4.1 | Submitted ideas visible to all employees | Query filter | Enables transparency |
| BR4.2 | Draft ideas visible only to owner/contributors | Query filter | Ensures privacy |
| BR4.3 | Ideas filtered by campaign | Query filter | Ensures campaign isolation |
| BR4.4 | Idea status always shown | Display logic | Enables tracking |
| BR4.5 | Submitter name always shown | Display logic | Ensures accountability |
| BR4.6 | Contributors list always shown | Display logic | Enables collaboration visibility |
| BR4.7 | Documents list always shown | Display logic | Enables resource access |
| BR4.8 | Submission date always shown | Display logic | Enables timeline tracking |
| BR4.9 | Evaluation scores shown only after period closes | Display logic | Ensures fair evaluation |
| BR4.10 | Ideas can be sorted by date, status, score | Query logic | Enables flexible viewing |
| BR4.11 | Ideas can be filtered by status | Query logic | Enables focused viewing |

### Category 5: Idea Editing Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR5.1 | Only submitter can edit submitted ideas | Authorization check | Ensures control |
| BR5.2 | Editing allowed only before evaluation period | Period check | Prevents mid-evaluation changes |
| BR5.3 | Contributors can edit if submitter allows | Permission grant | Enables collaboration |
| BR5.4 | Edit updates updatedAt timestamp | Auto-update | Enables tracking |
| BR5.5 | Edit history maintained | Audit logging | Enables traceability |
| BR5.6 | All required fields must be completed on edit | Validation | Ensures data quality |
| BR5.7 | Title must be unique on edit (excluding current) | DB constraint | Prevents duplicates |
| BR5.8 | Edit requires confirmation | UI confirmation | Prevents accidental changes |
| BR5.9 | Edit triggers audit log | Event logging | Enables compliance |
| BR5.10 | Edit notification sent to contributors | Event trigger | Ensures awareness |

### Category 6: Idea Deletion Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR6.1 | Only submitter can delete submitted ideas | Authorization check | Ensures control |
| BR6.2 | Deletion allowed only before evaluation period | Period check | Prevents mid-evaluation deletion |
| BR6.3 | Deletion requires confirmation | UI confirmation | Prevents accidental deletion |
| BR6.4 | Deleted ideas soft-deleted | Soft delete flag | Allows recovery |
| BR6.5 | Soft-deleted ideas permanently deleted after 30 days | Scheduled job | Cleanup old data |
| BR6.6 | Deletion triggers audit log | Event logging | Enables compliance |
| BR6.7 | Contributors notified of deletion | Event trigger | Ensures awareness |
| BR6.8 | Deleted ideas not visible in normal queries | Query filter | Ensures clean data |

### Category 7: Data Validation Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR7.1 | Title: 1-200 chars, alphanumeric + punctuation | Form validation | Ensures valid titles |
| BR7.2 | Description: 1-2000 chars, not whitespace only | Form validation | Ensures meaningful descriptions |
| BR7.3 | Expected Impact: High/Medium/Low only | Form validation | Ensures valid values |
| BR7.4 | Documents: Max 10 MB, allowed file types | File validation | Ensures security |
| BR7.5 | Documents: Max 5 per idea | Count validation | Prevents abuse |
| BR7.6 | Documents: Virus scanned before storage | Security check | Ensures safety |
| BR7.7 | All validation errors returned with details | Error handling | Enables user correction |
| BR7.8 | Validation errors include field name | Error handling | Enables user correction |
| BR7.9 | Validation errors include correction suggestions | Error handling | Enables user correction |

### Category 8: Status Transition Rules

| Rule ID | Rule | Enforcement | Impact |
|---------|------|-------------|--------|
| BR8.1 | Draft → Submitted (on explicit submit) | State machine | Enables submission |
| BR8.2 | Submitted → UnderEvaluation (on period start) | Scheduled job | Enables evaluation |
| BR8.3 | UnderEvaluation → Evaluated (on period end) | Scheduled job | Enables results |
| BR8.4 | Evaluated → Recognized (if top 3) | Recognition logic | Enables recognition |
| BR8.5 | Status transitions are one-way | State machine | Prevents invalid transitions |
| BR8.6 | Status changes logged in audit trail | Event logging | Enables traceability |
| BR8.7 | Status changes trigger notifications | Event trigger | Ensures awareness |

---

## Rule Enforcement Points

### Frontend Validation
- Title length and content
- Description length and content
- Expected Impact selection
- Required field completion
- File upload validation
- Confirmation dialogs

### Backend Validation
- All frontend validations repeated
- Database constraints enforced
- Authorization checks
- Campaign period validation
- User status validation
- Uniqueness constraints

### Database Constraints
- NOT NULL on required fields
- CHECK constraints on enums
- UNIQUE constraints on title (per campaign)
- FOREIGN KEY constraints on user/campaign
- CHECK constraints on field lengths

### Business Logic Validation
- Campaign submission period active
- User is active employee
- Submitter has Employee+ role
- Draft not already converted
- Contributor limit not exceeded
- Evaluation period not started

---

## Rule Priorities

### Critical Rules (Must Enforce)
- BR1.1, BR1.2, BR1.3 - Required fields
- BR1.6, BR1.7, BR1.8 - Authentication/Authorization
- BR1.9 - Campaign period validation
- BR3.1, BR3.2 - Contributor validation
- BR5.1, BR5.2 - Edit authorization
- BR6.1, BR6.2 - Delete authorization

### Important Rules (Should Enforce)
- BR1.4, BR1.5 - Data quality
- BR2.1 through BR2.10 - Draft management
- BR3.3 through BR3.13 - Contributor management
- BR4.1 through BR4.11 - Visibility rules
- BR7.1 through BR7.9 - Data validation

### Nice-to-Have Rules (Can Defer)
- BR2.7 - Permanent deletion after 90 days
- BR5.5 - Edit history maintenance
- BR5.10 - Edit notifications
- BR6.7 - Deletion notifications

---

## Rule Dependencies

### Dependent Rules
- BR1.9 depends on Campaign component providing period validation
- BR2.2 depends on scheduled job infrastructure
- BR3.2 depends on User component providing user status
- BR3.11 depends on Recognition component
- BR8.2, BR8.3 depend on scheduled job infrastructure

### Independent Rules
- BR1.1 through BR1.5 - Can be implemented independently
- BR2.1, BR2.3, BR2.4 - Can be implemented independently
- BR4.1 through BR4.11 - Can be implemented independently
- BR7.1 through BR7.9 - Can be implemented independently

---

## Rule Testing Strategy

### Unit Tests
- Test each rule in isolation
- Mock dependencies
- Test both valid and invalid cases
- Test boundary conditions

### Integration Tests
- Test rule interactions
- Test with real database
- Test with real user/campaign data
- Test error scenarios

### End-to-End Tests
- Test complete workflows
- Test all rules working together
- Test user scenarios
- Test edge cases

---

## Summary

**Total Rules**: 70+ business rules across 8 categories

**Critical Rules**: 12 rules that must be enforced
**Important Rules**: 40+ rules that should be enforced
**Nice-to-Have Rules**: 15+ rules that can be deferred

**Enforcement Points**: Frontend, Backend, Database, Business Logic

**Testing Strategy**: Unit, Integration, End-to-End tests
