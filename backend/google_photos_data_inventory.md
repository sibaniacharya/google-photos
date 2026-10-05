# Google Photos Data Inventory

This document audits the workspace for actual Google Photos public-feedback data, scanning all files, folders, and datasets across the entire `NextLeap/Graduation Project` workspace.

## Audit Findings

A comprehensive scan for keywords (`com.google.android.apps.photos`, `Google Photos`, `photos.google.com`, etc.) was performed across the workspace. All massive datasets (such as the 8,000-record dataset) were confirmed to be from different applications (e.g., WhatsApp, Myntra, Zomato).

The only legitimate Google Photos feedback data found resides in the current `backend` directory.

### Candidate 1: `backend/real_data.json`
* **File Path:** `backend/real_data.json`
* **Approximate Record Count:** 300
* **Source/Platform:** Google Play Store
* **Are records actually Google Photos feedback?:** YES (Verified via `source_url` containing `id=com.google.android.apps.photos`)
* **Are original source URLs preserved?:** YES
* **Are timestamps available?:** YES (e.g., `2026-09-21T15:19:02`)
* **Is it suitable for the incomplete-memory retrieval problem?:** POOR/PARTIAL. While it is genuine Google Photos data with high-quality metadata, a sample size of 300 random reviews is mathematically too small to yield a robust pool of candidates for the highly specific "incomplete memory retrieval" problem (as shown by our manual audit finding only 1 true positive in a 100-record subset).

### Candidate 2: `backend/extracted_records.json` & `backend/reclassified_records.json`
* **File Path:** `backend/extracted_records.json`, `backend/reclassified_records.json`
* **Approximate Record Count:** 100
* **Source/Platform:** Google Play Store
* **Are records actually Google Photos feedback?:** YES (These are just processed subsets of `real_data.json`)
* **Are original source URLs preserved?:** YES
* **Are timestamps available?:** YES
* **Is it suitable for the incomplete-memory retrieval problem?:** NO. (Already manually audited and rejected due to insufficient volume of true positives).

### Gaps or Missing Sources
* **Missing High-Volume Raw Corpus:** There is no ~10,000 record dataset of Google Photos reviews anywhere in the workspace. The only large corpus found was `normalized_reviews.json` (~8,000 records), which was confirmed to be WhatsApp data.
* **Missing Alternative Platforms:** There is no data from Reddit (e.g., `r/googlephotos`), Google Support Communities, or App Store reviews, which often contain more detailed "how do I find..." questions than 1-star Google Play rants.

---

## Status

**PARTIAL**

Some usable Google Photos feedback exists (the 300 records in `real_data.json`), but because the target cognitive problem (incomplete memory retrieval) is a rare edge-case in organic reviews, a much larger dataset (e.g., 5,000–10,000 records) or data from troubleshooting forums (Reddit/Support) is needed to build a viable research candidate pool. No such dataset currently exists in the workspace.
