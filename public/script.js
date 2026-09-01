/**
 * Sentinel AI 2.0 - Frontend Multi-Agent Controller & Streaming Client
 * Interacts with Swarm Orchestrator, SSE Telemetry, OCR Engine, and Remediation Tools.
 */

const API_BASE = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:5000";

// Preset Sample Library
const PRESET_SAMPLES = {
  fake_razorpay: "Dear Merchant, your Razorpay settlement of Rs 48,250 is on hold! To release payment instantly, verify merchant credentials at: https://razorpay-merchant-verification.xyz/login?id=94821. Failure will lead to permanent suspension. - Razorpay Risk Desk (support-rzp@okaxis)",
  upi_refund: "Congratulations! You have received a cashback refund of Rs. 3,499 for your failed Swiggy order. Scan the QR in GooglePay and enter your UPI PIN to claim immediately! Payee Handle: refund.support.desk@oksbi",
  sbi_kyc: "URGENT NOTICE: Dear Customer, your SBI YONO Netbanking access will be blocked today due to pending PAN/Aadhaar re-KYC. Click immediately to update: https://sbi-kyc-update-portal.online/auth or pay Rs. 1000 penalty.",
  job_deposit: "Hello Dear Candidate! Selected for Part-Time YouTube Reviewer Role. Earn Rs. 3,500 daily. To activate your task dashboard, deposit refundable registration fee of Rs. 999 to task.manager98@paytm. Join: https://t.me/parttime-daily-task-work",
  legit_invoice: "Hi Anshul, your payment of Rs 1,499 to Urban Company via Razorpay was successful! Payment ID: pay_Nq73Ks81JkLm90. View invoice at: https://razorpay.com/support/. Contact: support@razorpay.com."
};

let currentAnalysisData = null;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  setupPresetHandlers();
  setupImageDropzone();
});

// Preset Buttons
function setupPresetHandlers() {
  const buttons = document.querySelectorAll(".preset-btn");
  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const key = btn.getAttribute("data-preset");
      if (PRESET_SAMPLES[key]) {
        document.getElementById("messageInput").value = PRESET_SAMPLES[key];
      }
    });
  });
}

// Screenshot OCR Dropzone
function setupImageDropzone() {
  const imageInput = document.getElementById("imageInput");
  const fileStatus = document.getElementById("fileStatus");

  imageInput.addEventListener("change", async () => {
    const file = imageInput.files[0];
    if (!file) return;

    fileStatus.classList.remove("hidden");
    fileStatus.innerText = `Uploaded: ${file.name} (Extracting text via OCR...)`;

    const formData = new FormData();
    formData.append("image", file);

    try {
      logTelemetry("system", `Multimodal Vision: Uploaded screenshot '${file.name}'. Running Tesseract OCR...`);
      const res = await fetch(`${API_BASE}/api/analyze-image`, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      
      if (data.extracted_text) {
        document.getElementById("messageInput").value = data.extracted_text;
        fileStatus.innerText = `OCR Success: Extracted ${data.extracted_text.length} characters.`;
        renderSwarmResults(data);
      } else {
        fileStatus.innerText = "OCR: No readable text found.";
      }
    } catch (err) {
      fileStatus.innerText = "OCR error: Backend not reachable.";
    }
  });
}

// Main Swarm Investigation Runner (with SSE Telemetry Stream)
async function runSwarmInvestigation() {
  const message = document.getElementById("messageInput").value.trim();
  const btn = document.getElementById("analyzeBtn");

  if (!message) {
    alert("Please enter or paste a message to analyze.");
    return;
  }

  // Reset UI State
  btn.disabled = true;
  btn.innerHTML = `<span class="btn-icon">⚙️</span> <span class="btn-text">SWARM ACTIVE...</span>`;
  resetAgentNodes();
  clearTelemetry();

  const standbyCard = document.getElementById("standbyCard");
  const resultsContainer = document.getElementById("resultsContainer");
  if (standbyCard) standbyCard.classList.add("hidden");
  if (resultsContainer) resultsContainer.classList.remove("hidden");

  logTelemetry("system", `Swarm Orchestrator initialized. Target payload size: ${message.length} chars.`);

  // Attempt SSE Streaming Telemetry
  try {
    const eventSource = new EventSource(`${API_BASE}/api/analyze-stream?message=${encodeURIComponent(message)}`);
    
    eventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        handleStreamEvent(payload);
        
        if (payload.event === "FINAL_RESULT") {
          eventSource.close();
          renderSwarmResults(payload.data);
          btn.disabled = false;
          btn.innerHTML = `<span class="btn-icon">⚡</span> <span class="btn-text">DEPLOY AGENT SWARM</span>`;
        }
      } catch (e) {
        console.error("Error parsing stream event:", e);
      }
    };

    eventSource.onerror = async (err) => {
      console.warn("SSE stream interrupted. Falling back to REST API...", err);
      eventSource.close();
      await fallbackRestInvestigation(message);
      btn.disabled = false;
      btn.innerHTML = `<span class="btn-icon">⚡</span> <span class="btn-text">DEPLOY AGENT SWARM</span>`;
    };

  } catch (err) {
    console.warn("SSE unsupported, using standard fetch:", err);
    await fallbackRestInvestigation(message);
    btn.disabled = false;
    btn.innerHTML = `<span class="btn-icon">⚡</span> <span class="btn-text">DEPLOY AGENT SWARM</span>`;
  }
}

// Fallback Standard REST Execution
async function fallbackRestInvestigation(message) {
  try {
    const res = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    
    // Playback agent traces to console
    if (data.agent_traces) {
      data.agent_traces.forEach(trace => {
        logTelemetry(trace.type.toLowerCase(), `[${trace.agent}] ${trace.message}`);
      });
    }
    
    markAllAgentsComplete();
    renderSwarmResults(data);
  } catch (e) {
    logTelemetry("warning", `Backend connection failed: ${e.message}`);
    alert("Could not connect to Sentinel AI backend at " + API_BASE);
  }
}

// Stream Event Handler
function handleStreamEvent(event) {
  if (event.event === "AGENT_START") {
    setAgentStatus(event.agent, "RUNNING");
    logTelemetry("thought", `${event.icon || '🤖'} [${event.agent}] Dispatched and active.`);
  } else if (event.event === "AGENT_LOG") {
    logTelemetry(event.type.toLowerCase(), `[${event.agent}] ${event.message}`);
  } else if (event.event === "AGENT_COMPLETE") {
    setAgentStatus(event.agent, "COMPLETED");
  } else if (event.event === "ARBITRATION_START") {
    logTelemetry("decision", `⚖️ [Risk Arbitrator] ${event.message}`);
  }
}

// Render Final Multi-Agent Results
function renderSwarmResults(data) {
  currentAnalysisData = data;
  const panel = document.getElementById("resultsPanel");
  panel.classList.remove("hidden");

  // 1. Verdict & Badge
  document.getElementById("riskHeading").innerText = data.overall_risk || "Assessed";
  document.getElementById("recommendationBanner").innerText = data.recommendation || "";

  const badge = document.getElementById("riskBadgeLarge");
  badge.className = "risk-badge-large";
  if (data.risk_badge === "CRITICAL") {
    badge.innerText = "CRITICAL THREAT";
    badge.classList.add("badge-critical");
  } else if (data.risk_badge === "HIGH" || data.risk_badge === "MEDIUM") {
    badge.innerText = data.risk_badge + " RISK";
    badge.classList.add("badge-high");
  } else {
    badge.innerText = "VERIFIED SAFE";
    badge.classList.add("badge-safe");
  }

  // 2. Metrics & Progress Bars
  const conf = data.confidence_score || 0;
  document.getElementById("confidenceVal").innerText = `${conf}%`;
  const confBar = document.getElementById("confidenceBar");
  confBar.style.width = `${Math.max(conf, 5)}%`;
  if (data.risk_badge === "SAFE") {
    confBar.style.backgroundColor = "var(--accent-emerald)";
  } else if (conf >= 75) {
    confBar.style.backgroundColor = "var(--accent-red)";
  } else {
    confBar.style.backgroundColor = "var(--accent-cyan)";
  }

  const osint = data.vectors?.osint_risk || 0;
  document.getElementById("osintRiskVal").innerText = `${osint}%`;
  document.getElementById("osintBar").style.width = `${osint}%`;

  const web = data.vectors?.web_risk || 0;
  const webRiskEl = document.getElementById("webRiskVal");
  const webBarEl = document.getElementById("webBar");
  if (webRiskEl) webRiskEl.innerText = `${web}%`;
  if (webBarEl) webBarEl.style.width = `${web}%`;

  const fintech = data.vectors?.fintech_risk || 0;
  document.getElementById("fintechRiskVal").innerText = `${fintech}%`;
  document.getElementById("fintechBar").style.width = `${fintech}%`;

  const cog = data.vectors?.cognitive_risk || 0;
  document.getElementById("cognitiveRiskVal").innerText = `${cog}%`;
  document.getElementById("cognitiveBar").style.width = `${cog}%`;

  // 3. Findings Cards
  const findingsGrid = document.getElementById("findingsGrid");
  findingsGrid.innerHTML = "";
  if (data.analysis && data.analysis.length > 0) {
    data.analysis.forEach(item => {
      const card = document.createElement("div");
      card.className = "finding-card";
      const titleLower = item.title.toLowerCase();
      if (titleLower.includes("critical") || titleLower.includes("phishing") || titleLower.includes("trap") || titleLower.includes("spoof") || titleLower.includes("threat")) {
        card.classList.add("critical");
      } else if (titleLower.includes("verified") || titleLower.includes("authentic") || titleLower.includes("safe") || titleLower.includes("clean") || titleLower.includes("secure")) {
        card.classList.add("safe");
      }
      card.innerHTML = `<strong>${item.title}</strong><p>${item.text}</p>`;
      findingsGrid.appendChild(card);
    });
  }

  // 4. Autonomous Remediation Artifacts
  if (data.autonomous_actions) {
    // Cybercrime Complaint
    const comp = data.autonomous_actions.cybercrime_complaint?.complaint_draft || "No draft available.";
    document.getElementById("cybercrimeDraftText").innerText = comp;

    // Razorpay Abuse Notice
    const rzp = data.autonomous_actions.razorpay_abuse_takedown?.body || "No notice generated.";
    document.getElementById("takedownBodyText").innerText = rzp;

    // Playbook Steps
    const playbookContainer = document.getElementById("playbookSteps");
    playbookContainer.innerHTML = "";
    const steps = data.autonomous_actions.safety_playbook || [];
    steps.forEach(s => {
      const row = document.createElement("div");
      row.className = "playbook-step";
      row.innerHTML = `
        <div class="playbook-step-num">#${s.step}</div>
        <div class="playbook-step-content">
          <strong>${s.title}</strong>
          <span>${s.action}</span>
        </div>
      `;
      playbookContainer.appendChild(row);
    });
  }
}

// UI Agent Node Helper Functions
function resetAgentNodes() {
  ["osint", "web", "fintech", "cognitive", "defense"].forEach(key => {
    const node = document.getElementById(`node-${key}`);
    const status = document.getElementById(`status-${key}`);
    if (node) node.className = "agent-node";
    if (status) status.innerText = "READY";
  });
}

function setAgentStatus(agentName, status) {
  let key = "osint";
  if (agentName.includes("Web") || agentName.includes("Content")) key = "web";
  else if (agentName.includes("Fintech")) key = "fintech";
  else if (agentName.includes("Cognitive")) key = "cognitive";
  else if (agentName.includes("Action") || agentName.includes("Remediation") || agentName.includes("Defense")) key = "defense";

  const node = document.getElementById(`node-${key}`);
  const statusEl = document.getElementById(`status-${key}`);
  if (!node || !statusEl) return;
  
  if (status === "RUNNING") {
    node.className = "agent-node running";
    statusEl.innerText = "SCANNING";
  } else if (status === "COMPLETED") {
    node.className = "agent-node completed";
    statusEl.innerText = "DONE";
  }
}

function markAllAgentsComplete() {
  ["osint", "web", "fintech", "cognitive", "defense"].forEach(key => {
    const node = document.getElementById(`node-${key}`);
    const status = document.getElementById(`status-${key}`);
    if (node) node.className = "agent-node completed";
    if (status) status.innerText = "DONE";
  });
}

// Telemetry Console Helpers
function clearTelemetry() {
  document.getElementById("telemetryConsole").innerHTML = "";
}

function logTelemetry(type, message) {
  const consoleEl = document.getElementById("telemetryConsole");
  const item = document.createElement("div");
  item.className = `telemetry-item ${type}`;
  
  const time = new Date().toLocaleTimeString();
  item.innerHTML = `<span class="timestamp">[${time}]</span> ${escapeHtml(message)}`;
  consoleEl.appendChild(item);
  consoleEl.scrollTop = consoleEl.scrollHeight;
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Modal Helpers
function openModal(id) {
  document.getElementById(id).classList.remove("hidden");
}

function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
}

function copyText(elementId) {
  const text = document.getElementById(elementId).innerText;
  navigator.clipboard.writeText(text).then(() => {
    alert("Copied to clipboard!");
  });
}

// Export Forensic Evidence Dossier as JSON
function downloadIncidentDossier() {
  if (!currentAnalysisData) {
    alert("No active investigation data to export.");
    return;
  }
  const blob = new Blob([JSON.stringify(currentAnalysisData, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Sentinel_AI_Dossier_${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
