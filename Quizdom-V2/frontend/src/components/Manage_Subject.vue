<template>
  <!--
    Main admin layout for managing subjects and chapters.
    Includes navigation bar, search, and CRUD modals.
  -->
  <div class="d-flex flex-column min-vh-100 bg-sky text-dark bg-gradient-auth">
    <!-- Navigation Bar: Links to admin pages -->
    <nav class="navbar navbar-light px-4">
      <router-link class="navbar-brand fw-semibold display-6 text-dark" to="/admin">QUIZDOM Admin</router-link>  
      <div class="container-fluid d-flex justify-content-between align-items-center w-100">
        <ul class="navbar-nav d-flex flex-row gap-3 ms-auto">
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/manage_quiz">QUIZZES</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/manage_user">USERS</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/">🏠︎</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link bg-sky shadow-3d rounded px-3 py-1 nav-text-color fw-semibold" to="/admin_statistics">STATS 📊︎</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main Content: Subject management panel -->
    <main class="flex-grow-1 py-4">
      <div class="container">
        <!-- Page Heading -->
        <div class="container my-4">
          <h2 class="text-primary fw-bold">Manage Subjects</h2>
        </div>

        <!-- Search bar and Add Subject button -->
        <div class="container mt-4">
          <div class="row mb-4">
            <div class="col-md-8">
              <!-- Search input for filtering subjects -->
              <input 
                type="text" 
                class="form-control shadow-3d" 
                placeholder="Search subjects..." 
                v-model="searchQuery"
              >
            </div>
            <div class="col-md-4 text-end">
              <!-- Button to open Add Subject modal -->
              <button class="btn btn-primary shadow-3d" @click="addSubjectModal">
                + Add Subject
              </button>
            </div>
          </div>

          <!-- Show if no subjects match the search -->
          <div v-if="filteredSubjects.length === 0" class="text-center py-4">
            <p class="text-muted">No subjects found.</p>
          </div>

          <!-- List of subjects and their chapters -->
          <div v-else>
            <div 
              class="card mb-4 shadow-3d bg-sky" 
              v-for="subject in filteredSubjects" 
              :key="subject.subject_id"
            >
              <div class="card-body pb-3">
                <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center">
                  <!-- Subject name and description -->
                  <div class="mb-2 mb-md-0 me-md-3">
                    <h5 class="card-title text-primary mb-1">{{ subject.subject_name }}</h5>
                    <p class="card-text mb-0 text-muted">{{ subject.subject_description }}</p>
                  </div>
                  <!-- Edit/Delete subject buttons -->
                  <div class="d-flex gap-2">
                    <button class="btn btn-outline-primary btn-sm shadow-3d" @click="editSubjectModal(subject)">
                      ✎ Edit
                    </button>
                    <button class="btn btn-outline-danger btn-sm shadow-3d" @click="deleteSubject(subject.subject_id)">
                      ⛌ Delete
                    </button>
                  </div>
                </div>

                <!-- Table of chapters for this subject -->
                <table class="table table-hover mt-3">
                  <thead>
                    <tr>
                      <th>Chapter Name</th>
                      <th>Chapter Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="chapter in subject.chapters" :key="chapter.chapter_id">
                      <td>{{ chapter.chapter_name }}</td>
                      <td>{{ chapter.chapter_description }}</td>
                      <td>
                        <div class="d-flex gap-2">
                          <!-- Edit/Delete chapter buttons -->
                          <button class="btn btn-sm btn-outline-secondary shadow-3d" @click="editChapterModal(chapter)">
                            ✎
                          </button>
                          <button class="btn btn-sm btn-outline-secondary shadow-3d" @click="deleteChapter(chapter.chapter_id)">
                            ⛌
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <!-- Button to add a new chapter to this subject -->
                <button class="btn btn-outline-secondary btn-sm mt-2 shadow-3d" @click="addChapterModal(subject.subject_id)">
                  + 
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Add Subject Modal: Form for adding a new subject -->
    <div class="modal fade" id="addSubjectModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Subject</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSubject">
              <div class="mb-3">
                <label class="form-label">Subject Name</label>
                <input type="text" class="form-control" v-model="newSubject.subject_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" rows="3" v-model="newSubject.subject_description" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Add Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Subject Modal: Form for editing an existing subject -->
    <div class="modal fade" id="editSubjectModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Subject</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editSubject">
              <div class="mb-3">
                <label class="form-label">Subject Name</label>
                <input type="text" class="form-control" v-model="SelectedSubject.subject_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" rows="3" v-model="SelectedSubject.subject_description" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Update Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Chapter Modal: Form for adding a new chapter -->
    <div class="modal fade" id="addChapterModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Chapter</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addChapter">
              <div class="mb-3">
                <label class="form-label">Chapter Name</label>
                <input type="text" class="form-control" v-model="newChapter.chapter_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Chapter Description</label>
                <textarea class="form-control" rows="3" v-model="newChapter.chapter_description" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Add Chapter</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Chapter Modal: Form for editing an existing chapter -->
    <div class="modal fade" id="editChapterModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Chapter</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editChapter" @keydown.enter.prevent>
              <div class="mb-3">
                <label class="form-label">Chapter Name</label>
                <input type="text" class="form-control" v-model="SelectedChapter.chapter_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Chapter Description</label>
                <textarea class="form-control" rows="3" v-model="SelectedChapter.chapter_description" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Update Chapter</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    // Component state: holds all subjects, chapters, search/filter text, and form data
    data() {
        return {
            subjects: [], // All subjects fetched from backend (with chapters)
            searchQuery: '', // Search text for filtering subjects
            newSubject: { subject_name: '', subject_description: '' }, // Form data for adding subject
            newChapter: { subject_id: '', chapter_name: '', chapter_description: '' }, // Form data for adding chapter
            SelectedSubject: { subject_id: '', subject_name: '', subject_description: '' }, // Form data for editing subject
            SelectedChapter: { chapter_id: '', chapter_name: '', chapter_description: '' }, // Form data for editing chapter
        };
    },
    // Computed property to filter subjects by search query
    computed: {
        filteredSubjects() {
            return this.subjects.filter(subject => {
                return subject.subject_name.toLowerCase().includes(this.searchQuery.toLowerCase());
            });
        }
    },
    methods: {
        // Show the modal for adding a new subject
        addSubjectModal() {
            const modal = new bootstrap.Modal(document.getElementById('addSubjectModal'));
            modal.show();
        },
        // Send POST request to backend to add a new subject
        addSubject() {
            fetch('http://localhost:5000/add_subject/post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    subject_name: this.newSubject.subject_name,
                    subject_description: this.newSubject.subject_description
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
            })
            .then(data => {
                // Hide modal, clear form, alert user, and refresh subject list
                bootstrap.Modal.getInstance(document.getElementById('addSubjectModal')).hide();
                this.newSubject = { subject_name: '', subject_description: '' };
                alert(data.message);
                this.fetchSubjects();
            });
        },
        // Fetch all subjects (and their chapters) from backend
        fetchSubjects() {
            fetch('http://localhost:5000/add_subject/get', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                }
            })
            .then(response => response.json())
            .then(data => {
                this.subjects = data;
            });
        },
        // Show modal for editing a subject, pre-fill with selected subject data
        editSubjectModal(Subject) {
            this.SelectedSubject.subject_id = Subject.subject_id;
            this.SelectedSubject.subject_name = Subject.subject_name;
            this.SelectedSubject.subject_description = Subject.subject_description;
            const modal = new bootstrap.Modal(document.getElementById('editSubjectModal'));
            modal.show();
        },
        // Send PUT request to backend to update subject details
        editSubject() {
            fetch(`http://127.0.0.1:5000/edit_subject/${this.SelectedSubject.subject_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    subject_name: this.SelectedSubject.subject_name,
                    subject_description: this.SelectedSubject.subject_description
                })
            })
             .then(response => response.json()) 
             .then(data => {
                 alert(data.message);
                 bootstrap.Modal.getInstance(document.getElementById('editSubjectModal')).hide();
                 this.fetchSubjects();
             })
        },
        // Confirm and send DELETE request to remove a subject
        deleteSubject(subject_id) {
            if (!confirm('Are you sure you want to delete this subject?')) {
              return;
            }
            fetch (`http://127.0.0.1:5000/delete_subject/${subject_id}`, {
                method: 'DELETE',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                  subject_id: subject_id
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                this.fetchSubjects();
            })
        },
        // Show modal for adding a new chapter to a subject
        addChapterModal(subject_id) {
            this.newChapter.subject_id = subject_id;
            this.newChapter.chapter_name = '';
            this.newChapter.chapter_description = '';
            const modal = new bootstrap.Modal(document.getElementById('addChapterModal'));
            modal.show();
        },
        // Send POST request to backend to add a new chapter
        addChapter() {
            fetch(`http://127.0.0.1:5000/add_chapter/${this.newChapter.subject_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    chapter_name: this.newChapter.chapter_name,
                    chapter_description: this.newChapter.chapter_description
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                bootstrap.Modal.getInstance(document.getElementById('addChapterModal')).hide();
                this.fetchSubjects();
            });
        },
        // Show modal for editing a chapter, pre-fill with selected chapter data
        editChapterModal(Chapter) {
            this.SelectedChapter.chapter_id = Chapter.chapter_id;
            this.SelectedChapter.chapter_name = Chapter.chapter_name;
            this.SelectedChapter.chapter_description = Chapter.chapter_description;
            const modal = new bootstrap.Modal(document.getElementById('editChapterModal'));
            modal.show();
        },
        // Send PUT request to backend to update chapter details
        editChapter() {
            fetch(`http://127.0.0.1:5000/edit_chapter/${this.SelectedChapter.chapter_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    chapter_name: this.SelectedChapter.chapter_name,
                    chapter_description: this.SelectedChapter.chapter_description
                })
            })
             .then(response => response.json()) 
             .then(data => {
                 alert(data.message);
                 bootstrap.Modal.getInstance(document.getElementById('editChapterModal')).hide();
                 this.fetchSubjects();
             })
        },
        // Confirm and send DELETE request to remove a chapter
        deleteChapter(chapter_id) {
            if (!confirm('Are you sure you want to delete this chapter?')) {
              return;
            }
            fetch (`http://127.0.0.1:5000/delete_chapter/${chapter_id}`, {
                method: 'DELETE',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                  chapter_id: chapter_id
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                this.fetchSubjects();
            })
        }
    },
    // When the component is mounted, fetch all subjects from backend
    mounted() {
        this.fetchSubjects();
    }
};
</script>

<style scoped>
/* 
  Styles for the admin Manage Subjects page.
  Includes custom backgrounds, card shadows, and button hover effects.
*/
.bg-sky {
  background-color: #ffffff;
}
.bg-gradient-auth {
  background: linear-gradient(to bottom, #a1b1c9, #ffffff);
}
.shadow-3d {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 8px 20px rgba(0, 0, 0, 0.2);
}
.nav-link:hover {
  transform: translateY(-2px);
  transition: all 0.2s ease-in-out;
  background-color: #ffffff;
}
.nav-text-color {
  color: #667589;
}
</style>
