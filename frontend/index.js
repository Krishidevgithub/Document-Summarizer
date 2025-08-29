let uploadHistory = JSON.parse(localStorage.getItem("pdfHistory")) || [];
let currentFile = null;

// Page navigation
function showPage(pageId, event) {
  document
    .querySelectorAll(".page")
    .forEach((page) => page.classList.remove("active"));
  document
    .querySelectorAll(".nav-tab")
    .forEach((tab) => tab.classList.remove("active"));

  document.getElementById(pageId).classList.add("active");
  if (event) event.target.classList.add("active");

  if (pageId === "history") displayHistory();
}

// Initialize upload area
function initUploadArea() {
  const uploadArea = document.querySelector(".upload-area");
  const fileInput = document.getElementById("fileInput");
  const generateBtn = document.getElementById("generateBtn");

  uploadArea.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));

  generateBtn.addEventListener("click", generateSummary);
}

// Handle file validation
function handleFile(file) {
  hideError();
  if (!file) return;
  
  if (file.type !== "application/pdf") {
    showError("Only PDF files are allowed.");
    return;
  }

  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    showError("File size must be less than 10MB.");
    return;
  }

  currentFile = file;
  displayFileInfo(file);
  
  const generateBtn = document.getElementById("generateBtn");
  const summaryBox = document.getElementById("summaryBox");
  
  generateBtn.style.display = "inline-block";
  summaryBox.style.display = "none";
}

// Display file info
function displayFileInfo(file) {
  document.getElementById("fileName").textContent = `📄 ${file.name}`;
  document.getElementById("fileSize").textContent = `Size: ${(file.size / 1024 / 1024).toFixed(2)} MB`;
  document.getElementById("fileInfo").style.display = "block";
}

// Generate summary
async function generateSummary() {
  if (!currentFile) {
    showError("Please select a PDF file first.");
    return;
  }

  const generateBtn = document.getElementById("generateBtn");
  const summaryBox = document.getElementById("summaryBox");
  const summaryContent = document.getElementById("summaryContent");

  generateBtn.innerHTML = '<span class="loading"></span>Generating...';
  generateBtn.disabled = true;

  try {
    const formData = new FormData();
    formData.append("file", currentFile);

    const response = await fetch("http://localhost:8000/upload-resume", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let errMsg = "Failed to generate summary.";
      try {
        const errData = await response.json();
        if (errData.detail) errMsg = errData.detail;
      } catch {}
      throw new Error(errMsg);
    }

    const result = await response.json();

    let summaryText = "";
    if (result.summary && result.summary.trim() !== "") {
      summaryText = result.summary;
    } else if (result.top_words && result.top_words.length > 0) {
      summaryText = "Top keywords (fallback): " + result.top_words.join(", ");
    } else {
      summaryText = "No summary available.";
    }

    summaryContent.innerHTML = `
      <strong>Document Analysis Complete!</strong><br><br>
      📊 <strong>File:</strong> ${currentFile.name}<br>
      📅 <strong>Processed:</strong> ${new Date().toLocaleString()}<br><br>
      🤖 <strong>Summary:</strong><br>
      <p style="margin-top: 10px;">${summaryText}</p>
    `;

    summaryBox.style.display = "block";
    addToHistory(currentFile, summaryText);
    summaryBox.scrollIntoView({ behavior: "smooth" });

  } catch (err) {
    showError(err.message || "Error generating summary. Please try again.");
  } finally {
    generateBtn.innerHTML = "Generate Summary";
    generateBtn.disabled = false;
  }
}

// Add to history (store summary too, keep ALL history)
function addToHistory(file, summaryText) {
  const historyItem = {
    name: file.name,
    size: file.size,
    date: new Date().toISOString(),
    timestamp: Date.now(),
    summary: summaryText
  };
  uploadHistory.unshift(historyItem);
  // ❌ Removed the line that was trimming history to 50 items
  localStorage.setItem("pdfHistory", JSON.stringify(uploadHistory));
}

// Display history
function displayHistory() {
  const historyContent = document.getElementById("historyContent");

  if (uploadHistory.length === 0) {
    historyContent.innerHTML =
      '<div class="empty-history">No uploads yet. Upload your first PDF to get started!</div>';
    return;
  }

  historyContent.innerHTML = uploadHistory
    .map((item, index) => {
      const date = new Date(item.date);
      return `
        <div class="history-item">
          <div class="history-item-name">📄 ${item.name}</div>
          <div class="history-item-date">Uploaded on ${date.toLocaleDateString()} at ${date.toLocaleTimeString()} • ${(item.size / 1024 / 1024).toFixed(2)} MB</div>
          <button class="show-summary-btn" onclick="showSummaryFromHistory(${index})">Show Summary</button>
        </div>
      `;
    })
    .join("");
}

// Show summary from history click (redirects to Home page)
function showSummaryFromHistory(index) {
  const item = uploadHistory[index];
  if (!item) return;

  showPage("home");

  const summaryBox = document.getElementById("summaryBox");
  const summaryContent = document.getElementById("summaryContent");

  summaryContent.innerHTML = `
    <strong>📄 ${item.name}</strong><br>
    📅 Uploaded: ${new Date(item.date).toLocaleString()}<br><br>
    🤖 <strong>Summary:</strong><br>
    <p style="margin-top: 10px;">${item.summary || "No summary saved."}</p>
  `;

  summaryBox.style.display = "block";
  summaryBox.scrollIntoView({ behavior: "smooth" });
}

// Show/Hide error
function showError(msg) {
  const errDiv = document.getElementById("errorMessage");
  errDiv.textContent = msg;
  errDiv.style.display = "block";
}

function hideError() {
  document.getElementById("errorMessage").style.display = "none";
}

// Initialize everything
document.addEventListener("DOMContentLoaded", () => {
  initUploadArea();
  displayHistory();
  testBackendConnectivity();
});

// Test backend connectivity
async function testBackendConnectivity() {
  try {
    const response = await fetch("http://localhost:8000/");
    if (response.ok) {
      console.log("Backend is accessible");
    } else {
      console.warn("Backend responded with error:", response.status);
    }
  } catch (err) {
    console.error("Cannot connect to backend:", err);
    showError("Warning: Cannot connect to backend server. Please make sure it's running on localhost:8000");
  }
}
