# Unit 1: Idea Submission & Management - Domain Entities

## Overview
This document defines all domain entities for the Idea Submission & Management unit, including their attributes, relationships, and database schema.

---

## Entity Definitions

### 1. Idea Entity

**Purpose**: Represents a submitted innovative idea

**Attributes**:
```
id: UUID
  - Primary key
  - Auto-generated
  - Immutable

title: String
  - Required
  - Length: 1-200 characters
  - Unique within campaign
  - Indexed for search

description: String
  - Required
  - Length: 1-2000 characters
  - Supports markdown formatting
  - Indexed for full-text search

expectedImpact: Enum
  - Required
  - Values: HIGH, MEDIUM, LOW
  - Indexed for filtering

submitterId: UUID
  - Required
  - Foreign key to User
  - Indexed for user's ideas query
  - Immutable after creation

campaignId: UUID
  - Required
  - Foreign key to Campaign
  - Indexed for campaign filtering
  - Immutable after creation

status: Enum
  - Required
  - Values: DRAFT, SUBMITTED, UNDER_EVALUATION, EVALUATED, RECOGNIZED
  - Default: DRAFT
  - Indexed for status filtering
  - Updated by system

createdAt: DateTime
  - Required
  - Auto-set on creation
  - Immutable
  - Indexed for sorting

updatedAt: DateTime
  - Required
  - Auto-set on creation
  - Updated on any modification
  - Indexed for sorting

submittedAt: DateTime
  - Optional
  - Set when idea is submitted
  - Immutable after set
  - Indexed for timeline queries

recognizedAt: DateTime
  - Optional
  - Set when idea wins recognition
  - Immutable after set
  - Indexed for recognition queries

contributors: List<Contributor>
  - One-to-many relationship
  - Lazy loaded
  - Includes submitter implicitly

documents: List<Document>
  - One-to-many relationship
  - Lazy loaded
  - Max 5 documents
```

**Database Schema**:
```sql
CREATE TABLE ideas (
  id UUID PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  expected_impact VARCHAR(20) NOT NULL CHECK (expected_impact IN ('HIGH', 'MEDIUM', 'LOW')),
  submitter_id UUID NOT NULL REFERENCES users(id),
  campaign_id UUID NOT NULL REFERENCES campaigns(id),
  status VARCHAR(20) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'SUBMITTED', 'UNDER_EVALUATION', 'EVALUATED', 'RECOGNIZED')),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  submitted_at TIMESTAMP,
  recognized_at TIMESTAMP,
  deleted_at TIMESTAMP,
  
  UNIQUE(campaign_id, title),
  INDEX idx_submitter_id (submitter_id),
  INDEX idx_campaign_id (campaign_id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at),
  INDEX idx_campaign_status (campaign_id, status)
);
```

---

### 2. Draft Entity

**Purpose**: Represents a work-in-progress idea

**Attributes**:
```
id: UUID
  - Primary key
  - Auto-generated
  - Immutable

userId: UUID
  - Required
  - Foreign key to User
  - Indexed for user's drafts query
  - Immutable after creation

ideaData: JSON
  - Required
  - Contains partial idea data
  - Schema: {
      title?: string,
      description?: string,
      expectedImpact?: string,
      contributors?: UUID[],
      documents?: UUID[]
    }
  - Flexible schema for partial data

createdAt: DateTime
  - Required
  - Auto-set on creation
  - Immutable
  - Indexed for sorting

updatedAt: DateTime
  - Required
  - Auto-set on creation
  - Updated on any modification
  - Indexed for sorting

expiresAt: DateTime
  - Required
  - Set to 30 days from creation
  - Indexed for expiration queries
  - Immutable after set

convertedToIdeaId: UUID
  - Optional
  - Set when draft is converted to idea
  - Foreign key to Idea
  - Immutable after set

deletedAt: DateTime
  - Optional
  - Set when draft is deleted (soft delete)
  - Indexed for soft delete queries
  - Immutable after set
```

**Database Schema**:
```sql
CREATE TABLE drafts (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  idea_data JSON NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  converted_to_idea_id UUID REFERENCES ideas(id),
  deleted_at TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_expires_at (expires_at),
  INDEX idx_deleted_at (deleted_at)
);
```

---

### 3. Contributor Entity

**Purpose**: Represents a person contributing to an idea

**Attributes**:
```
id: UUID
  - Primary key
  - Auto-generated
  - Immutable

ideaId: UUID
  - Required
  - Foreign key to Idea
  - Indexed for idea's contributors query
  - Immutable after creation

userId: UUID
  - Required
  - Foreign key to User
  - Indexed for user's contributions query
  - Immutable after creation

addedAt: DateTime
  - Required
  - Auto-set on creation
  - Immutable
  - Indexed for sorting

addedBy: UUID
  - Required
  - Foreign key to User (who added them)
  - Indexed for audit trail
  - Immutable after creation

deletedAt: DateTime
  - Optional
  - Set when contributor is removed (soft delete)
  - Indexed for soft delete queries
  - Immutable after set
```

**Database Schema**:
```sql
CREATE TABLE contributors (
  id UUID PRIMARY KEY,
  idea_id UUID NOT NULL REFERENCES ideas(id),
  user_id UUID NOT NULL REFERENCES users(id),
  added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  added_by UUID NOT NULL REFERENCES users(id),
  deleted_at TIMESTAMP,
  
  UNIQUE(idea_id, user_id),
  INDEX idx_idea_id (idea_id),
  INDEX idx_user_id (user_id),
  INDEX idx_deleted_at (deleted_at)
);
```

---

### 4. Document Entity

**Purpose**: Represents a file attached to an idea

**Attributes**:
```
id: UUID
  - Primary key
  - Auto-generated
  - Immutable

ideaId: UUID
  - Required
  - Foreign key to Idea
  - Indexed for idea's documents query
  - Immutable after creation

fileName: String
  - Required
  - Original file name
  - Length: 1-255 characters
  - Immutable after creation

fileSize: Long
  - Required
  - File size in bytes
  - Max: 10 MB (10485760 bytes)
  - Immutable after creation

fileType: String
  - Required
  - MIME type (e.g., application/pdf)
  - Immutable after creation

uploadedAt: DateTime
  - Required
  - Auto-set on creation
  - Immutable
  - Indexed for sorting

uploadedBy: UUID
  - Required
  - Foreign key to User
  - Indexed for audit trail
  - Immutable after creation

storageUrl: String
  - Required
  - Cloud storage URL (S3, Azure Blob, etc.)
  - Immutable after creation

storageKey: String
  - Required
  - Storage provider's object key
  - Immutable after creation

virusScanStatus: Enum
  - Required
  - Values: PENDING, CLEAN, INFECTED
  - Default: PENDING
  - Updated after scan

virusScanedAt: DateTime
  - Optional
  - Set after virus scan completes
  - Immutable after set

deletedAt: DateTime
  - Optional
  - Set when document is deleted (soft delete)
  - Indexed for soft delete queries
  - Immutable after set
```

**Database Schema**:
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  idea_id UUID NOT NULL REFERENCES ideas(id),
  file_name VARCHAR(255) NOT NULL,
  file_size BIGINT NOT NULL CHECK (file_size <= 10485760),
  file_type VARCHAR(100) NOT NULL,
  uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  uploaded_by UUID NOT NULL REFERENCES users(id),
  storage_url VARCHAR(2048) NOT NULL,
  storage_key VARCHAR(2048) NOT NULL,
  virus_scan_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (virus_scan_status IN ('PENDING', 'CLEAN', 'INFECTED')),
  virus_scanned_at TIMESTAMP,
  deleted_at TIMESTAMP,
  
  INDEX idx_idea_id (idea_id),
  INDEX idx_virus_scan_status (virus_scan_status),
  INDEX idx_deleted_at (deleted_at)
);
```

---

## Entity Relationships

### Idea ↔ User (Submitter)
- **Type**: Many-to-One
- **Cardinality**: Many ideas → One user
- **Foreign Key**: Idea.submitterId → User.id
- **Cascade**: No cascade delete (preserve audit trail)

### Idea ↔ Campaign
- **Type**: Many-to-One
- **Cardinality**: Many ideas → One campaign
- **Foreign Key**: Idea.campaignId → Campaign.id
- **Cascade**: No cascade delete (preserve audit trail)

### Idea ↔ Contributor
- **Type**: One-to-Many
- **Cardinality**: One idea → Many contributors
- **Foreign Key**: Contributor.ideaId → Idea.id
- **Cascade**: Cascade soft delete (mark as deleted)

### Idea ↔ Document
- **Type**: One-to-Many
- **Cardinality**: One idea → Many documents
- **Foreign Key**: Document.ideaId → Idea.id
- **Cascade**: Cascade soft delete (mark as deleted)

### Contributor ↔ User (Contributor)
- **Type**: Many-to-One
- **Cardinality**: Many contributors → One user
- **Foreign Key**: Contributor.userId → User.id
- **Cascade**: No cascade delete (preserve audit trail)

### Contributor ↔ User (Added By)
- **Type**: Many-to-One
- **Cardinality**: Many contributors → One user
- **Foreign Key**: Contributor.addedBy → User.id
- **Cascade**: No cascade delete (preserve audit trail)

### Document ↔ User (Uploaded By)
- **Type**: Many-to-One
- **Cardinality**: Many documents → One user
- **Foreign Key**: Document.uploadedBy → User.id
- **Cascade**: No cascade delete (preserve audit trail)

### Draft ↔ User
- **Type**: Many-to-One
- **Cardinality**: Many drafts → One user
- **Foreign Key**: Draft.userId → User.id
- **Cascade**: Cascade delete (drafts are temporary)

### Draft ↔ Idea (Converted)
- **Type**: One-to-One
- **Cardinality**: One draft → One idea (optional)
- **Foreign Key**: Draft.convertedToIdeaId → Idea.id
- **Cascade**: No cascade delete (preserve audit trail)

---

## Entity Lifecycle

### Idea Lifecycle
```
Created (DRAFT)
  ↓
Submitted (SUBMITTED)
  ↓
Under Evaluation (UNDER_EVALUATION)
  ↓
Evaluated (EVALUATED)
  ↓
Recognized (RECOGNIZED) [optional]
  ↓
Deleted (soft delete)
```

### Draft Lifecycle
```
Created
  ↓
Updated (multiple times)
  ↓
Converted to Idea OR Expired OR Deleted
  ↓
Permanently Deleted (after 90 days)
```

### Contributor Lifecycle
```
Added
  ↓
Active (can edit idea)
  ↓
Removed (soft delete) OR Idea Deleted
  ↓
Permanently Deleted (after 30 days)
```

### Document Lifecycle
```
Uploaded
  ↓
Virus Scan (PENDING → CLEAN/INFECTED)
  ↓
Active (if CLEAN)
  ↓
Deleted (soft delete) OR Idea Deleted
  ↓
Permanently Deleted (after 30 days)
```

---

## Data Integrity Rules

### Referential Integrity
- All foreign keys must reference valid records
- Soft deletes do not break referential integrity
- Cascade soft deletes for related records

### Uniqueness Constraints
- Idea title unique within campaign
- Contributor unique per idea (one user per idea)
- Draft unique per user (one active draft per user)

### Check Constraints
- Idea status must be valid enum value
- Expected impact must be valid enum value
- File size must not exceed 10 MB
- Document count must not exceed 5 per idea
- Contributor count must not exceed 10 per idea

### Temporal Constraints
- createdAt ≤ updatedAt
- submittedAt ≥ createdAt (if set)
- recognizedAt ≥ submittedAt (if set)
- expiresAt = createdAt + 30 days (for drafts)
- deletedAt ≥ createdAt (if set)

---

## Indexing Strategy

### Primary Indexes
- Idea.id (primary key)
- Draft.id (primary key)
- Contributor.id (primary key)
- Document.id (primary key)

### Foreign Key Indexes
- Idea.submitterId
- Idea.campaignId
- Contributor.ideaId
- Contributor.userId
- Document.ideaId
- Document.uploadedBy
- Draft.userId

### Query Optimization Indexes
- Idea.status (for status filtering)
- Idea.created_at (for sorting)
- Idea.(campaign_id, status) (composite for filtering)
- Draft.expires_at (for expiration queries)
- Draft.deleted_at (for soft delete queries)
- Contributor.deleted_at (for soft delete queries)
- Document.virus_scan_status (for scan status queries)

### Full-Text Search Indexes
- Idea.title (for search)
- Idea.description (for full-text search)

---

## Summary

**Entities**: 4 core entities (Idea, Draft, Contributor, Document)

**Relationships**: 7 relationships (mostly Many-to-One)

**Attributes**: 40+ total attributes across all entities

**Constraints**: Referential integrity, uniqueness, check, temporal

**Indexes**: 15+ indexes for query optimization

**Lifecycle**: Clear state transitions for each entity

**Data Integrity**: Comprehensive rules to maintain data quality
