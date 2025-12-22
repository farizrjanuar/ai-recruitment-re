# DELETE Feature Documentation

## Overview
Fitur DELETE telah ditambahkan ke aplikasi AI Recruitment untuk memungkinkan penghapusan Job Position dan Candidate secara permanen. Fitur ini mencakup backend API endpoints dan frontend UI dengan confirmation dialogs.

## Backend Implementation

### 1. Job Deletion

#### Endpoint
```
DELETE /api/jobs/<job_id>
```

#### Response
- **200 OK**: Job berhasil dihapus
```json
{
  "message": "Job position deleted successfully",
  "job_id": "uuid-here"
}
```

- **404 Not Found**: Job tidak ditemukan
```json
{
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "Job position with ID <job_id> not found"
  }
}
```

- **500 Internal Server Error**: Error saat menghapus
```json
{
  "error": {
    "code": "DELETE_ERROR",
    "message": "Error message here"
  }
}
```

#### Implementation Details
- **File**: `backend/services/job_service.py`
- **Method**: `delete_job(job_id: str) -> Tuple[bool, Optional[str]]`
- **Features**:
  - Hard delete (bukan soft delete)
  - Cascade delete untuk semua `match_results` terkait
  - Transaction rollback jika terjadi error
  - Validasi job existence sebelum delete

- **File**: `backend/routes/job_routes.py`
- **Endpoint**: `@job_bp.route('/<job_id>', methods=['DELETE'])`
- **Features**:
  - Proper HTTP status codes
  - Error handling dengan error codes
  - RESTful response format

### 2. Candidate Deletion

#### Endpoint
```
DELETE /api/candidates/<candidate_id>
```

#### Response
- **200 OK**: Candidate berhasil dihapus
```json
{
  "message": "Candidate deleted successfully",
  "candidate_id": "uuid-here"
}
```

- **404 Not Found**: Candidate tidak ditemukan
```json
{
  "error": {
    "code": "CANDIDATE_NOT_FOUND",
    "message": "Candidate with ID <candidate_id> not found"
  }
}
```

- **500 Internal Server Error**: Error saat menghapus
```json
{
  "error": {
    "code": "DELETE_ERROR",
    "message": "Error message here"
  }
}
```

#### Implementation Details
- **File**: `backend/services/candidate_service.py`
- **Method**: `delete_candidate(candidate_id: str) -> Tuple[bool, Optional[str]]`
- **Features**:
  - Hard delete dari database
  - Menghapus file CV dari filesystem
  - Cascade delete untuk semua `match_results` terkait
  - Transaction rollback jika terjadi error
  - Cleanup file system jika ada error

- **File**: `backend/routes/candidate_routes.py`
- **Endpoint**: `@candidate_bp.route('/<candidate_id>', methods=['DELETE'])`
- **Features**:
  - Proper HTTP status codes
  - Error handling dengan error codes
  - RESTful response format

## Frontend Implementation

### 1. API Service Layer

#### Job API
- **File**: `src/services/jobAPI.js`
- **Method**: `deleteJob(jobId)`
```javascript
deleteJob: async (jobId) => {
  const response = await api.delete(`/jobs/${jobId}`);
  return response.data;
}
```

#### Candidate API
- **File**: `src/services/candidateAPI.js`
- **Method**: `deleteCandidate(candidateId)`
```javascript
deleteCandidate: async (candidateId) => {
  const response = await api.delete(`/candidates/${candidateId}`);
  return response.data;
}
```

### 2. User Interface

#### JobList.js
- **Location**: `src/pages/JobList.js`
- **Features**:
  - Delete button pada setiap job card
  - Confirmation dialog menggunakan `window.confirm()`
  - Auto-refresh list setelah delete berhasil
  - Error handling dengan error message display
  - Menampilkan nama job di confirmation dialog

#### JobDetail.js
- **Location**: `src/pages/JobDetail.js`
- **Features**:
  - Delete button di header actions
  - Confirmation dialog dengan nama job
  - Redirect ke `/jobs` setelah delete berhasil
  - Error handling dengan error state

#### CandidateList.js
- **Location**: `src/pages/CandidateList.js`
- **Features**:
  - Delete button pada setiap row table
  - Confirmation dialog dengan nama candidate
  - Auto-refresh list setelah delete
  - Error handling dengan error message
  - Styling inline untuk spacing

#### CandidateDetail.js
- **Location**: `src/pages/CandidateDetail.js`
- **Features**:
  - Delete button di header actions
  - Confirmation dialog dengan nama candidate
  - Redirect ke `/candidates` setelah delete berhasil
  - Error handling dengan error state
  - Updated layout dengan flexbox header

### 3. Styling

#### Delete Button Style
All CSS files include consistent delete button styling:

```css
.btn-delete {
  background: #dc3545;  /* Red color */
  color: white;
  padding: 6px-10px (varies by context);
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s;
}

.btn-delete:hover {
  background: #c82333;  /* Darker red on hover */
}
```

**Modified Files**:
- `src/pages/JobList.css`
- `src/pages/JobDetail.css`
- `src/pages/CandidateList.css`
- `src/pages/CandidateDetail.css`

## User Flow

### Delete Job
1. User navigates to Job List (`/jobs`) atau Job Detail (`/jobs/:id`)
2. User clicks "Delete" button
3. Confirmation dialog appears: "Are you sure you want to delete '{job_title}'? This action cannot be undone."
4. If user clicks OK:
   - API call ke `DELETE /api/jobs/<job_id>`
   - Success: List refreshes (JobList) atau redirect ke /jobs (JobDetail)
   - Error: Error message ditampilkan
5. If user clicks Cancel: No action taken

### Delete Candidate
1. User navigates to Candidate List (`/candidates`) atau Candidate Detail (`/candidates/:id`)
2. User clicks "Delete" button
3. Confirmation dialog appears: "Are you sure you want to delete '{candidate_name}'? This action cannot be undone."
4. If user clicks OK:
   - API call ke `DELETE /api/candidates/<candidate_id>`
   - Success: List refreshes (CandidateList) atau redirect ke /candidates (CandidateDetail)
   - Error: Error message ditampilkan
5. If user clicks Cancel: No action taken

## Database Impact

### Cascade Delete
Kedua Job dan Candidate memiliki cascade delete untuk `match_results`:

**Job Deletion**:
- Menghapus job_position record
- Auto-delete semua match_results dengan `job_id` terkait

**Candidate Deletion**:
- Menghapus candidate record
- Menghapus CV file dari filesystem (`backend/uploads/`)
- Auto-delete semua match_results dengan `candidate_id` terkait

### Model Configuration
CASCADE delete sudah dikonfigurasi di SQLAlchemy models:

```python
# In JobPosition model
matches = db.relationship('MatchResult', 
                         backref='job_position', 
                         lazy=True, 
                         cascade='all, delete-orphan')

# In Candidate model
matches = db.relationship('MatchResult', 
                         backref='candidate', 
                         lazy=True, 
                         cascade='all, delete-orphan')
```

## Security Considerations

1. **No Authentication**: Aplikasi tidak memiliki authentication, jadi siapa saja bisa delete data
2. **No Soft Delete**: Ini adalah hard delete, data tidak bisa di-recover
3. **Confirmation Dialog**: Browser-based confirmation sebagai safety measure
4. **Transaction Rollback**: Database transaction akan rollback jika terjadi error

## Testing Checklist

- [ ] Create job via UI → Delete dari JobList → Verify job hilang dari database
- [ ] Create job via UI → View detail → Delete dari JobDetail → Verify redirect dan job terhapus
- [ ] Upload CV via UI → Delete dari CandidateList → Verify candidate dan CV file terhapus
- [ ] Upload CV via UI → View detail → Delete dari CandidateDetail → Verify redirect dan data terhapus
- [ ] Delete job yang memiliki match results → Verify cascade delete bekerja
- [ ] Delete candidate yang memiliki match results → Verify cascade delete bekerja
- [ ] Test error handling: Try delete non-existent ID via API
- [ ] Test confirmation dialog: Click Cancel → Verify no action taken
- [ ] Test UI refresh after delete in list views

## Known Limitations

1. **No Undo**: Tidak ada undo functionality, delete adalah permanent
2. **No Bulk Delete**: User harus delete satu per satu
3. **Browser Confirmation Only**: Menggunakan `window.confirm()` standard browser, bukan custom modal
4. **No Audit Log**: Tidak ada logging untuk delete operations

## Future Enhancements

1. Add soft delete option dengan "deleted_at" timestamp
2. Add audit logging untuk track delete operations
3. Add bulk delete functionality
4. Implement custom confirmation modal dengan better UX
5. Add "Restore" functionality untuk soft-deleted items
6. Add permission/role checking untuk delete operations
