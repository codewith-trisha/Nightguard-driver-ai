# 🛡️ NightGuard AI: Real-Time Driver Drowsiness & Fatigue Monitoring System

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![Status](https://img.shields.io/badge/Project_Status-Complete-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

> **NightGuard AI** is an advanced, dual-layered computer vision safety system engineered to detect driver fatigue and prevent micro-sleep traffic accidents in real time. The solution bridges a high-performance **Python OpenCV core tracking engine** with an **interactive web analytics dashboard** for live telemetry, scenario stress-testing, and presentation evaluation.

---

## 📌 Executive Summary & System Architecture

Driver fatigue and microsleeps account for a critical percentage of severe roadway accidents. **NightGuard AI** operates continuously by capturing live frame streams, isolating spatial sub-regions of interest (ROIs), and evaluating temporal eye-closure geometry to trigger multi-stage safety interventions before a hazard occurs.

### End-to-End Processing Pipeline

```text
  ┌────────────────────────────────┐
  │      Video Input Capture       │
  │  (RGB Webcam / NIR IR Stream)  │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │   Spatial Feature Detection    │
  │  (OpenCV Haar Cascade Face/Eye)│
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │   Region of Interest (ROI)     │
  │     Cropping & Normalization   │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │ Eye Aspect Ratio (EAR) & PERCLOS│
  │      Temporal Accumulation     │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │  Multi-Tier Escalation Logic   │
  │ (Active ➔ Warning ➔ Alert)     │
  └───────────────┬────────────────┘
                  │
                  ▼
  ┌────────────────────────────────┐
  │   Multi-Modal Output Action    │
  │ (Web Telemetry / Pygame Siren) │
  └────────────────────────────────┘

## 🚀 Key Features

* **Real-Time Computer Vision:** Utilizes OpenCV and Haar cascade classifiers to track facial regions and eye states continuously via webcam feed.
* **Duration-Based Alerting:** Implements time-to-closure thresholds that escalate warnings (active monitoring $\rightarrow$ eyes closed warning $\rightarrow$ critical sleep alert).
* **Interactive Web Dashboard (`AI.html`):** A modern, dark-themed command center featuring live video overlays, dynamic telemetry metric cards, and a real-time Eye Aspect Ratio (EAR) trend chart.
* **Simulation Testing Modes:** Allows evaluation under multiple preset scenarios (Normal Driving, Eyes Closed, Critical Sleep, and Yawning).
* **Web Audio API Alarms:** Synthesized multi-stage buzzer alerts generated directly in browser JavaScript without external audio dependencies.
* **IR Night-Vision Simulation:** Built-in CSS filter toggle simulating near-infrared cabin monitoring under low-light or night-driving conditions.

---

## 🛠️ Tech Stack

| Domain | Tech Stack |
| **Programming Language** | Python 3.13, JavaScript (ES6+) |
| **Computer Vision & Processing** | OpenCV (`opencv-python`), NumPy |
| **Frontend & Analytics** | HTML5, Tailwind CSS, Chart.js, FontAwesome |
| **Audio & Signals** | Web Audio API, Pygame (optional local audio) |

---

## 📐 Mathematical Formulation (Eye Aspect Ratio)

To compute eye openness accurately across varying head poses, the system measures the **Eye Aspect Ratio (EAR)** using 6 facial keypoints per eye:

$$\text{EAR} = \frac{\Vert{}p_2 - p_6\Vert{} + \Vert{}p_3 - p_5\Vert{}}{2 \Vert{}p_1 - p_4\Vert{}}$$

Where:
* $p_1, p_4$ represent horizontal corner coordinates of the eye.
* $p_2, p_3, p_5, p_6$ represent vertical boundary landmark coordinates.
* Under normal open-eye conditions, $\text{EAR}$ remains stable ($\approx 0.28 - 0.35$). Upon eye closure, $\text{EAR} \rightarrow 0$.

---

## 📂 Project Structure

```text
nightguard-driver-ai/
│
├── drowsiness_detector.py           # Real-time Python CV webcam detector
├── AI.html                          # Interactive web dashboard & presentation landing page
├── haarcascade_frontalface_default.xml # OpenCV face detection cascade
├── haarcascade_eye.xml              # OpenCV eye detection cascade
├── requirements.txt                 # Python project dependencies
└── README.md                        # Project documentation & presentation guide
