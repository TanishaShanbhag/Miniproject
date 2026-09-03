# 🧬 Type 2 Diabetes Risk Prediction System

A web-based Type 2 Diabetes Risk Prediction System that combines clinical health parameters with genetic risk factors to estimate an individual's diabetes risk.

## 📌 Overview

This project provides an interactive dashboard where users can enter health and genetic information and receive a diabetes risk prediction.

The system considers clinical parameters such as:

- Age
- BMI
- Glucose
- Insulin
- HOMA
- Leptin
- Adiponectin
- Resistin
- MCP.1

It also incorporates three genetic risk-allele features:

- RA_SNP1
- RA_SNP2
- RA_SNP3

The backend processes the input data and returns a prediction along with a risk percentage and risk category.

## ✨ Features

- 🧬 Genetic and clinical risk-factor analysis
- 📊 Diabetes risk percentage estimation
- 🔎 Low, Medium, and High risk classification
- 🖥️ Interactive web dashboard
- ⚡ Flask-based REST API
- 🌐 React-based frontend
- 🔗 Frontend-backend integration using API requests
- 📱 User-friendly interface for entering patient information

##🏗️ Project Structure

```text
Diabetes_project/
│
├── Backend/
│   ├── app.py
│   ├── gene.csv
│   ├── MODEL_README.txt
│   ├── requirements.txt
│
├── Frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── demo.mp4
└── README.md
