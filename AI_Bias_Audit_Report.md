# 🛡️ AI Algorithmic Bias Audit Report: Booking System

**Project:** AI Governance Audit Toolkit
**Auditor:** Senior Architect (ESCP)
**Date:** 2026-03-29
**Status:** 🚩 HIGH RISK DETECTED

---

## 1. Executive Summary
This audit investigated potential price discrimination within the automated booking system. Analysis of 1,000 transaction logs revealed a systematic price markup targeting users on premium devices (Mac/iPhone).

## 2. Audit Evidence (SQL Results)
Using SQL-based data forensics, we calculated the average final price across different user segments:

| Device Type | Avg Final Price | Risk Level |
| :--- | :--- | :--- |
| **iPhone** | **341.62** | 🔴 Critical |
| **Mac** | **339.19** | 🔴 Critical |
| **Windows** | 305.54 | 🟢 Baseline |
| **Android** | 304.59 | 🟢 Baseline |

**Finding:** Mac and iPhone users are being overcharged by approximately **11% - 12%** compared to Windows/Android users.

## 3. Legal & Regulatory Risk
Under the **EU AI Act (Article 10: Data and Data Governance)**, this behavior constitutes:
* **Proxy Discrimination**: Using device type as a surrogate for socioeconomic status.
* **Unfair Trade Practice**: Lack of transparency in dynamic pricing algorithms.

## 4. Strategic Recommendations
1. **Bias Mitigation**: Adjust the weights of the 'device_type' feature in the ML model.
2. **Transparency**: Implement a "Price Explainability" feature for users.
3. **Continuous Monitoring**: Setup automated alerts for 'Disparate Impact Ratio' drift.
