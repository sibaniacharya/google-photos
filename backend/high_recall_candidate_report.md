# High-Recall Candidate Discovery Report

## Overview
- **Total Source Records:** 2,022
- **Number of Candidates Selected:** 300

## Candidate Selection Methodology
A high-recall, non-evaluative keyword matching approach was used to scan the full 2,022-record corpus. The goal was strictly to generate a broad candidate pool for subsequent AI semantic extraction, not to identify confirmed problems at this stage.

Records were prioritized based on the presence of terms from two broad signal groups. We selected up to 300 records with the highest signal density, heavily favoring records that contained at least one search intent signal AND one memory/object signal to ensure diversity across retrieval intents and memory cues.

## Signal Groups Used
1. **Search & Action Intent:** `can't find`, `cannot find`, `looking for`, `trying to find`, `where is`, `find my`, `lost`, `missing`, `disappeared`, `search`, `locate`, `can't locate`
2. **Memory & Object Cues:** `old photo`, `old picture`, `previous photo`, `memories`, `memory`, `remember`, `forgot`, `forgotten`, `trip`, `vacation`, `birthday`, `wedding`, `school`, `college`, `family`, `friend`, `baby`, `child`, `place`, `location`, `screenshot`, `document`, `receipt`, `medicine`, `food`, `car`, `house`, `event`, `clothes`, `shirt`, `dress`, `color`, `appearance`

## Candidate Distribution
- **Search Intent + Memory Cues (Both):** 83
- **Search Intent Only:** 53
- **Memory Cues Only:** 164

## Examples of Candidate Types
* **Search for Events:** e.g., "looking for wedding photos"
* **Missing People/Places:** e.g., "family vacation pictures missing"
* **Forgotten Specifics:** e.g., "can't find screenshots of receipts"
* **Broad Memory Retrieval:** e.g., "searching for old memories"

## Limitations & Disclaimer
- **High Recall, Low Precision:** A keyword match does **NOT** mean the record is a retrieval problem. For example, the word "lost" might refer to losing a phone, and "search" might refer to praise for the search feature.
- **No Confirmation:** At this stage, NO candidates are claimed to be confirmed opportunities. The candidate pool is exclusively a high-recall input for the next AI semantic extraction stage.
- **Traceability Preserved:** The original review text, dates, ratings, and URLs have been strictly preserved with no alteration.
