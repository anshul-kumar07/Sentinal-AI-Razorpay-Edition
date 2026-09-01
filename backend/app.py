"""
Sentinel AI 2.0 - Flask Backend API & Multi-Agent Server
Provides REST endpoints and Server-Sent Events (SSE) for Autonomous Swarm Forensics.
"""

import os
import sys
import json
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
from PIL import Image

from core.orchestrator import SwarmOrchestrator

FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

orchestrator = SwarmOrchestrator()

# OCR Initialization (RapidOCR pure python/ONNX engine with pytesseract fallback)
rapid_ocr_engine = None
try:
    from rapidocr_onnxruntime import RapidOCR
    rapid_ocr_engine = RapidOCR()
except Exception:
    rapid_ocr_engine = None


def reconstruct_natural_lines(ocr_result) -> str:
    """Groups OCR bounding boxes into natural horizontal lines and sorts words left-to-right."""
    import numpy as np
    if not ocr_result:
        return ""

    boxes = []
    for item in ocr_result:
        if not item or len(item) < 2 or not item[1].strip():
            continue
        pts = np.array(item[0])
        y_min = float(np.min(pts[:, 1]))
        y_max = float(np.max(pts[:, 1]))
        y_center = (y_min + y_max) / 2.0
        x_min = float(np.min(pts[:, 0]))
        height = max(y_max - y_min, 1.0)
        boxes.append({
            "text": item[1].strip(),
            "y_center": y_center,
            "x_min": x_min,
            "height": height
        })

    if not boxes:
        return ""

    # Sort boxes primarily by vertical center
    boxes = sorted(boxes, key=lambda b: b["y_center"])
    median_h = np.median([b["height"] for b in boxes])
    line_threshold = max(median_h * 0.65, 12.0)

    lines = []
    current_line = []
    for b in boxes:
        if not current_line:
            current_line.append(b)
        else:
            line_y_avg = np.mean([item["y_center"] for item in current_line])
            if abs(b["y_center"] - line_y_avg) <= line_threshold:
                current_line.append(b)
            else:
                sorted_line = sorted(current_line, key=lambda x: x["x_min"])
                lines.append(" ".join(item["text"] for item in sorted_line))
                current_line = [b]

    if current_line:
        sorted_line = sorted(current_line, key=lambda x: x["x_min"])
        lines.append(" ".join(item["text"] for item in sorted_line))

    # Filter out empty or pure-menu lines if present
    filtered = []
    for line in lines:
        clean = line.strip()
        if clean and clean.lower() not in ["file edit view", "file edit view h1"]:
            filtered.append(clean)

    return "\n".join(filtered)


def extract_text_from_image_safe(image_file) -> tuple[str, str | None]:
    """Safely extracts text using RapidOCR (or Tesseract fallback) from uploaded image."""
    try:
        if hasattr(image_file, "read"):
            image_bytes = image_file.read()
        elif isinstance(image_file, str) and os.path.exists(image_file):
            with open(image_file, "rb") as f:
                image_bytes = f.read()
        else:
            return "", "Invalid image file format."

        # 1. Try RapidOCR
        if rapid_ocr_engine is not None:
            import numpy as np
            import cv2
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is not None:
                ocr_result, _ = rapid_ocr_engine(img)
                if ocr_result:
                    natural_text = reconstruct_natural_lines(ocr_result)
                    if natural_text:
                        return natural_text.strip(), None

        # 2. Try pytesseract fallback
        try:
            import pytesseract
            import io
            img_pil = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(img_pil)
            if text.strip():
                return text.strip(), None
        except Exception:
            pass

        return "", "Could not detect clear readable text in the image."
    except Exception as e:
        return "", f"OCR extraction error: {str(e)}"


def get_frontend_file(filename: str):
    candidates = [
        os.path.join(PROJECT_ROOT, "frontend", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", filename),
        os.path.join(os.getcwd(), "frontend", filename),
        os.path.join(os.getcwd(), filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return os.path.join(FRONTEND_DIR, filename)


# ---------------- WEB & API ENDPOINTS ----------------

@app.route("/", methods=["GET"])
def index():
    """Serves the main Cyber Defense Console UI directly."""
    return send_file(get_frontend_file("index.html"))


@app.route("/style.css", methods=["GET"])
def style_css():
    return send_file(get_frontend_file("style.css"), mimetype="text/css")


@app.route("/script.js", methods=["GET"])
def script_js():
    return send_file(get_frontend_file("script.js"), mimetype="application/javascript")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "system": "Sentinel AI 2.0 - Autonomous Multi-Agent Cyber Defense Platform",
        "status": "OPERATIONAL",
        "version": "2.0.0",
        "hackathon": "Razorpay Buildathon",
        "active_agents": [
            "OSINT & Network Intelligence Agent",
            "Live Web & Content Forensic Agent",
            "Fintech & Payment Forensic Agent",
            "Cognitive & Social Engineering Agent",
            "Autonomous Action & Defense Agent"
        ]
    })


@app.route("/analyze", methods=["POST"])
@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Synchronous Multi-Agent Investigation Endpoint.
    Accepts JSON payload: {"message": "..."}
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "No message provided for analysis."}), 400

    try:
        report = orchestrator.run_investigation(message)
        return jsonify(report)
    except Exception as e:
        return jsonify({
            "error": "Investigation pipeline encountered an error.",
            "details": str(e)
        }), 500


@app.route("/api/analyze-stream", methods=["GET", "POST"])
def analyze_stream():
    """
    Server-Sent Events (SSE) Streaming Endpoint.
    Yields live thoughts, tool invocations, and agent telemetry in real-time.
    """
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()
    else:
        message = request.args.get("message", "").strip()

    if not message:
        return jsonify({"error": "No message provided"}), 400

    def generate_events():
        for event_data in orchestrator.stream_investigation(message):
            yield f"data: {json.dumps(event_data)}\n\n"
            time.sleep(0.05)  # Smooth delivery for visual effect

    return Response(generate_events(), mimetype="text/event-stream")


@app.route("/analyze-image", methods=["POST"])
@app.route("/api/analyze-image", methods=["POST"])
def analyze_image():
    """
    Multimodal OCR Endpoint. Extracts text from uploaded screenshot and runs Swarm Forensics.
    """
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "No image file uploaded."}), 400

    extracted_text, error = extract_text_from_image_safe(image)

    if error or not extracted_text:
        # Fallback response if OCR text is empty
        return jsonify({
            "extracted_text": extracted_text,
            "overall_risk": "Unverified (Image unreadable)",
            "confidence_score": 0,
            "analysis": [{
                "title": "OCR Processing Status",
                "text": error or "Could not detect clear alphanumeric characters in the uploaded image. Please paste the text directly."
            }],
            "recommendation": "Paste the message text directly into the console for deep forensic analysis.",
            "vectors": {"osint_risk": 0, "fintech_risk": 0, "cognitive_risk": 0},
            "autonomous_actions": {"safety_playbook": []},
            "agent_traces": []
        })

    # Run full Swarm investigation on the extracted text
    report = orchestrator.run_investigation(extracted_text)
    report["extracted_text"] = extracted_text
    return jsonify(report)


@app.route("/api/demo-samples", methods=["GET"])
def get_demo_samples():
    """
    Provides curated test scenarios for quick 1-click judging during the Buildathon demo.
    """
    samples = [
        {
            "id": "fake_razorpay",
            "title": "Fake Razorpay Gateway Phishing",
            "category": "Fintech / Brand Impersonation",
            "text": "Dear Merchant, your Razorpay settlement of Rs 48,250 is on hold! To release payment instantly, verify merchant credentials at: https://razorpay-merchant-verification.xyz/login?id=94821. Failure will lead to permanent suspension. - Razorpay Risk Desk (support-rzp@okaxis)"
        },
        {
            "id": "upi_refund_trap",
            "title": "UPI 'Enter PIN to Receive' Scam",
            "category": "UPI / Payment Fraud",
            "text": "Congratulations! You have received a cashback refund of Rs. 3,499 for your failed Swiggy order. Scan the QR in GooglePay and enter your UPI PIN to claim immediately! Payee Handle: refund.support.desk@oksbi"
        },
        {
            "id": "sbi_kyc_panic",
            "title": "SBI NetBanking Block Panic SMS",
            "category": "Banking / Social Engineering",
            "text": "URGENT NOTICE: Dear Customer, your SBI YONO Netbanking access will be blocked today due to pending PAN/Aadhaar re-KYC. Click immediately to update: https://sbi-kyc-update-portal.online/auth or pay Rs. 1000 penalty."
        },
        {
            "id": "telegram_job_deposit",
            "title": "Telegram Job Daily Payout Bait",
            "category": "Employment / Advance Fee",
            "text": "Hello Dear Candidate! Selected for Part-Time YouTube Reviewer Role. Earn Rs. 3,500 daily. To activate your task dashboard, deposit refundable registration fee of Rs. 999 to task.manager98@paytm. Join: https://t.me/parttime-daily-task-work"
        },
        {
            "id": "legit_razorpay_receipt",
            "title": "Verified Razorpay Payment Receipt",
            "category": "Legitimate Transaction",
            "text": "Hi Anshul, your payment of Rs 1,499 to Urban Company via Razorpay was successful! Payment ID: pay_Nq73Ks81JkLm90. View invoice at: https://pages.razorpay.com/pl_verified_merchant/receipt. Contact: support@razorpay.com."
        }
    ]
    return jsonify(samples)


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

if __name__ == "__main__":
    print("=========================================================")
    print(" [*] Sentinel AI 2.0 - Autonomous Multi-Agent Platform")
    print(" [*] Active for Razorpay Buildathon Evaluation")
    print(" [*] Server running at: http://127.0.0.1:5000")
    print("=========================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)
