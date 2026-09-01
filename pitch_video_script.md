# 🎬 Sentinel AI 2.0 – 5-Minute Hackathon Pitch Video Script
**Submission for Razorpay Buildathon | Agentic AI Hiring Hackathon**

---

## ⏱️ Video Timeline Breakdown (5 Minutes Total)

```
[0:00 - 0:50]  PART 1: The Origin (Sentinel 1.0) & The Problem in Fintech (50s)
[0:50 - 1:45]  PART 2: The Quantum Leap – Transforming into Sentinel 2.0 (55s)
[1:45 - 3:30]  PART 3: Live Interactive Demo on Screen (105s)
               ├─ 1:45 - 2:30 : Attack 1: Fake Razorpay Gateway & Auto-Takedown Notice
               ├─ 2:30 - 3:00 : Attack 2: Multimodal Screenshot OCR Vision
               └─ 3:00 - 3:30 : Test 3  : Ground-Truth Safe Message Verification
[3:30 - 4:15]  PART 4: Razorpay Synergy & Fraud Mitigation Impact (45s)
[4:15 - 5:00]  PART 5: Tech Stack, Engineering Highlights & Closing (45s)
```

---

## 📊 Quick Comparison: Sentinel AI 1.0 vs Sentinel AI 2.0

| Feature | Sentinel AI 1.0 (Prototype) | Sentinel AI 2.0 (Agentic Buildathon Edition) |
|---|---|---|
| **Core Architecture** | Single-script static regex & keyword rules (`if "pay" in text`) | **Autonomous Multi-Agent Swarm** with 4 specialized collaborative agents |
| **Domain & OSINT Intelligence** | Basic `.xyz` string checks | **Levenshtein edit distance**, live DNS resolver, and brand typosquatting tools |
| **Fintech & Payment Forensics** | None (treated all links the same) | **Razorpay gateway validator** (`pages.razorpay.com`), UPI VPA inspector, and PIN paradox detector |
| **Action & Remediation** | Passive static score on screen | **Autonomous Remediation Agent** generating CERT-In complaint dossiers & `abuse@razorpay.com` takedown notices |
| **Telemetry & Observability** | No logs or internal visibility | **Real-Time Server-Sent Events (SSE)** streaming live agent thoughts and tool invocations |
| **Multimodal OCR Vision** | Fragile external Tesseract dependency | **RapidOCR ONNX Neural Vision** running 100% in-memory with zero system dependencies |

---

## 🎙️ Word-for-Word Speaking Script & Screen Actions

### 🟢 PART 1: The Origin (Sentinel 1.0) & The Problem (0:00 – 0:50)
**Screen:** Camera on your face / Intro slide with title **Sentinel AI 2.0**.

> *"Hello everyone and the Razorpay AI team! My name is Anshul, and today I’m thrilled to present **Sentinel AI 2.0**—an Autonomous Multi-Agent Cyber & Fintech Fraud Defense Platform built for the Razorpay Buildathon.*
> 
> *A few weeks ago, I built **Sentinel AI 1.0** as a fun prototype to detect basic scam messages. But Sentinel 1.0 had a huge fundamental limitation: it relied on static keyword checks like `if 'pay' in message: score += 25`.*
> 
> *In the real world—especially across the Indian digital payments ecosystem where over 1.3 million scams occur yearly—fraud is far more sophisticated. Scammers create pixel-perfect **spoofed Razorpay payment pages**, manipulate users with **UPI collect-request traps** claiming 'Enter UPI PIN to receive refund', and engineer panic with fake Bank KYC block threats.*
> 
> *Static rules and single LLM prompts fail because modern fraud operates across **Network Infrastructure**, **Payment Mechanics**, and **Cognitive Psychology** simultaneously."*

---

### 🟢 PART 2: The Quantum Leap – What We Upgraded in Sentinel 2.0 (0:50 – 1:45)
**Screen:** Show the **Architecture Diagram** and the **1.0 vs 2.0 Comparison Table**.

> *"For the Razorpay Buildathon, I completely re-architected Sentinel from the ground up into **Sentinel AI 2.0**—transforming it from a static script into an **Autonomous Multi-Agent Swarm** coordinated by a Central Supervisor:*
> 
> 1. *First, the **OSINT & Network Intelligence Agent** uses algorithmic tools to detect brand typosquatting using Levenshtein distance, inspects suspicious TLDs, and performs safe DNS resolution.*
> 2. *Second, the **Fintech & Payment Forensic Agent** verifies authentic Razorpay checkout endpoints (`pages.razorpay.com`), unmasks spoofed merchant VPAs on personal bank handles (`support-rzp@okaxis`), and flags NPCI architectural paradoxes.*
> 3. *Third, the **Cognitive Reasoning Agent** evaluates artificial urgency vectors, panic countdowns, and institutional authority coercion.*
> 4. *And most importantly, the **Autonomous Action & Defense Agent** moves beyond passive scoring to **autonomous remediation**: auto-generating CERT-In complaint dossiers and formal brand takedown notices for `abuse@razorpay.com`.*
> 
> *Let's see Sentinel 2.0 in action!"*

---

### 🟢 PART 3: Live Interactive Demo (1:45 – 3:30)
**Screen:** Browser open at `http://localhost:5000`.

#### 🎯 Demo 1: Fake Razorpay Gateway Phishing & Takedown (1:45 – 2:30)
**Action:** Click preset **`🎯 Fake Razorpay Phishing`** and click **`⚡ DEPLOY AGENT SWARM`**.

> *"Let's test an attack scenario targeting merchants: an urgent email claiming a Razorpay settlement is blocked, linking to `razorpay-merchant-verification.xyz` with a fake VPA `support-rzp@okaxis`.*
> 
> *When I deploy the swarm, look at the UI: the 4 agent nodes activate simultaneously. In the real-time telemetry stream below, you can see live thought traces and tool executions streaming over Server-Sent Events (SSE).*
> 
> *The Swarm arbitrates the consensus as **Critical Scam / Phishing (85% Confidence)**.*
> *And look at the Autonomous Remediation Hub: with one click on **'Razorpay Abuse Notice'**, Sentinel has generated a formal brand abuse takedown email pre-addressed to `abuse@razorpay.com` with the offending IoCs and registrar details pre-populated!"*

#### 📸 Demo 2: Multimodal Screenshot Vision (2:30 – 3:00)
**Action:** Click **`Upload / Drop Screenshot`** and select the Swiggy refund scam screenshot.

> *"In Sentinel 1.0, OCR was fragile and often crashed. In Sentinel 2.0, we built an **ONNX Neural Vision Engine** that runs 100% in-memory.*
> *When I upload a raw screenshot of a WhatsApp message, Sentinel parses the text in natural reading order, analyzes the payment mechanics, and flags the core rule: 'UPI PIN is strictly for debiting funds, never to receive money.'*
> *It also builds an official **CERT-In (1930 Helpline)** complaint payload ready for law enforcement submission."*

#### ✅ Demo 3: Zero False Positives / Safe Verification (3:00 – 3:30)
**Action:** Click preset **`✅ Legit Invoice`** and click **`⚡ DEPLOY AGENT SWARM`**.

> *"A robust defense system must also avoid false alarms. When I test an authentic Razorpay receipt from `pages.razorpay.com`, the swarm validates the official domain, checks payment mechanics, and outputs an emerald green **VERIFIED SAFE (0% Risk)** verdict with positive confirmation evidence."*

---

### 🟢 PART 4: Razorpay Synergy & Fraud Mitigation Impact (3:30 – 4:15)
**Screen:** Camera on face / Dashboard overview.

> *"Why is Sentinel AI 2.0 a strategic superpower for Razorpay?*
> 
> 1. *It directly integrates with **Razorpay Shield & Thirdwatch** to detect fake checkout clones and protect merchants from brand spoofing before customers lose money.*
> 2. *It stops UPI payment reversal scams by enforcing NPCI payment architecture rules.*
> 3. *It reduces incident response and brand abuse takedown triage time from hours to seconds through autonomous dossier generation."*

---

### 🟢 PART 5: Tech Stack & Strong Closing (4:15 – 5:00)
**Screen:** Camera on face with VS Code in the background.

> *"Under the hood, Sentinel AI 2.0 is built with **Python 3.14**, a modular **Multi-Agent Orchestration Engine**, **RapidOCR ONNX Vision**, and **Server-Sent Events (SSE)**.*
> *It runs 100% locally with zero external API dependencies, while remaining fully plug-and-play with foundation LLMs like Gemini or OpenAI.*
> 
> *Taking an idea from a simple script into a production-grade autonomous agent swarm reflects my passion for AI engineering. I would love the opportunity to bring this energy, rapid prototyping ability, and agentic AI focus to the Razorpay AI team as an AI Intern.*
> 
> *Thank you, and I look forward to building the future of autonomous fintech AI at Razorpay!"*
