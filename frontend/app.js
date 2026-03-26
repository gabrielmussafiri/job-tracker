const API = "https://job-tracker-xjbi.onrender.com";

// ── Auth helpers ─────────────────────────
function getUserId() {
  return localStorage.getItem("user_id");
}

function goToDashboard() {
  window.location.href = "dashboard.html";
}

function goToAddJob() {
  window.location.href = "add-job.html";
}

// ── Register ─────────────────────────────
async function register() {
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  const message = document.getElementById("register-message");

  const response = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
    message.className = "success";
    message.textContent = "Account created! You can now login.";
  } else {
    message.className = "error";
    message.textContent = data.error;
  }
}

// ── Login ─────────────────────────────────
async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  const message = document.getElementById("login-message");

  const response = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
    // Save user_id in localStorage
    localStorage.setItem("user_id", data.user_id);
    goToDashboard();
  } else {
    message.className = "error";
    message.textContent = data.error;
  }
}

// ── Logout ────────────────────────────────
function logout() {
  localStorage.removeItem("user_id");
  window.location.href = "login.html";
}

// ── Load dashboard ────────────────────────
async function loadDashboard() {
  const user_id = getUserId();
  if (!user_id) return (window.location.href = "login.html");

  await loadStats(user_id);
  await loadJobs(user_id);
}

// ── Load stats ────────────────────────────
async function loadStats(user_id) {
  const response = await fetch(`${API}/jobs/stats?user_id=${user_id}`);
  const data = await response.json();

  document.getElementById("total").textContent = data.total;
  document.getElementById("applied").textContent = data.applied;
  document.getElementById("interview").textContent = data.interview;
  document.getElementById("offer").textContent = data.offer;
  document.getElementById("rejected").textContent = data.rejected;
}

// ── Load jobs ─────────────────────────────
async function loadJobs(user_id) {
  const response = await fetch(`${API}/jobs/?user_id=${user_id}`);
  const jobs = await response.json();
  const container = document.getElementById("jobs-list");

  if (jobs.length === 0) {
    container.innerHTML = "<p>No jobs yet. Add your first one!</p>";
    return;
  }

  container.innerHTML = jobs
    .map(
      (job) => `
        <div class="job-card">
            <div class="job-info">
                <h3>${job.company}</h3>
                <p>${job.role}</p>
            </div>
            <div>
                <span class="status ${job.status}">${job.status}</span>
                <button class="danger" onclick="deleteJob(${job.id})">Delete</button>
            </div>
        </div>
    `,
    )
    .join("");
}

// ── Add job ───────────────────────────────
async function addJob() {
  const user_id = getUserId();
  if (!user_id) return (window.location.href = "login.html");

  const company = document.getElementById("company").value;
  const role = document.getElementById("role").value;
  const status = document.getElementById("status").value;
  const message = document.getElementById("message");

  const response = await fetch(`${API}/jobs/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company, role, status, user_id: parseInt(user_id) }),
  });

  const data = await response.json();

  if (response.ok) {
    message.className = "success";
    message.textContent = "Job added successfully!";
    document.getElementById("company").value = "";
    document.getElementById("role").value = "";
  } else {
    message.className = "error";
    message.textContent = data.error;
  }
}

// ── Delete job ────────────────────────────
async function deleteJob(job_id) {
  const user_id = getUserId();

  await fetch(`${API}/jobs/${job_id}`, {
    method: "DELETE",
  });

  await loadJobs(user_id);
  await loadStats(user_id);
}

// ── Auto load dashboard ───────────────────
if (window.location.pathname.includes("dashboard")) {
  loadDashboard();
}
