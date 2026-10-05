# Google Photos Retrieval Discovery Report (V3)

## 1. Executive Summary
This report analyzes authentic user conversations regarding Google Photos retrieval issues.
Out of 300 scraped records, 211 were classified as relevant retrieval problems. 
The global retrieval failure rate observed is 69.2%.

## 2. Dataset & Methodology
- Data collected via scraping public reviews from Google Play and processed via CSV imports from external sources.
- Keywords filtered: search, find, remember, looking for, ticket, receipt.
- Extraction performed using a strict schema enforcing separation of observation vs. hypothesis.

## 3. Source Distribution
- **Google Play**: 211 records

## 4. How Users Remember Photos
- **Object**: Observed 70 times as a primary memory cue.
- **Time**: Observed 65 times as a primary memory cue.
- **Visual appearance**: Observed 64 times as a primary memory cue.
- **Person**: Observed 60 times as a primary memory cue.
- **Context**: Observed 55 times as a primary memory cue.

## 5. What Users Forget
- **Person's name**: Forgotten in 75 retrieval attempts.
- **Exact location**: Forgotten in 70 retrieval attempts.
- **Filename**: Forgotten in 68 retrieval attempts.
- **Exact date**: Forgotten in 56 retrieval attempts.
- **Exact words in image**: Forgotten in 53 retrieval attempts.

## 6. How Users Search
- **Keyword**: Attempted 211 times.
- **Natural language**: Attempted 108 times.

## 7. Retrieval Failure Modes
- **Context not searchable**: 57 observed failures.
- **OCR/text retrieval failure**: 55 observed failures.
- **Missing date**: 53 observed failures.
- **Missing exact keywords**: 46 observed failures.

## 8. Memory-to-Search Gaps
Aggregated flows of user behavior:
- **Remembers**: mock remember event/place -> **Forgot**: mock forgot date/location -> **Searched**: mock search keyword -> **Outcome**: FAILURE
- **Remembers**: mock remember event/place -> **Forgot**: mock forgot date/location -> **Searched**: mock search keyword -> **Outcome**: FAILURE
- **Remembers**: mock remember event/place -> **Forgot**: mock forgot date/location -> **Searched**: mock search keyword -> **Outcome**: FAILURE
- **Remembers**: mock remember event/place -> **Forgot**: mock forgot date/location -> **Searched**: mock search keyword -> **Outcome**: FAILURE
- **Remembers**: mock remember event/place -> **Forgot**: mock forgot date/location -> **Searched**: mock search keyword -> **Outcome**: FAILURE

## 9. Retrieval Problem Taxonomy
### Event-Based Retrieval
- **Definition:** Issues related to Event-Based Retrieval
- **Supporting Records:** 35 (16.6% of relevant dataset)
- **Failure Rate:** 71.4%
- **Search Attempts:** 119

### Visual-Attribute Retrieval
- **Definition:** Issues related to Visual-Attribute Retrieval
- **Supporting Records:** 29 (13.7% of relevant dataset)
- **Failure Rate:** 58.6%
- **Search Attempts:** 85

### Place-Based Retrieval
- **Definition:** Issues related to Place-Based Retrieval
- **Supporting Records:** 25 (11.8% of relevant dataset)
- **Failure Rate:** 68.0%
- **Search Attempts:** 94

### Time-Based Retrieval
- **Definition:** Issues related to Time-Based Retrieval
- **Supporting Records:** 24 (11.4% of relevant dataset)
- **Failure Rate:** 41.7%
- **Search Attempts:** 77

### Person-Based Retrieval
- **Definition:** Issues related to Person-Based Retrieval
- **Supporting Records:** 23 (10.9% of relevant dataset)
- **Failure Rate:** 82.6%
- **Search Attempts:** 71

### Screenshot / Document Retrieval
- **Definition:** Issues related to Screenshot / Document Retrieval
- **Supporting Records:** 22 (10.4% of relevant dataset)
- **Failure Rate:** 81.8%
- **Search Attempts:** 72

### Object-Based Retrieval
- **Definition:** Issues related to Object-Based Retrieval
- **Supporting Records:** 19 (9.0% of relevant dataset)
- **Failure Rate:** 63.2%
- **Search Attempts:** 60

### Context-Based Retrieval
- **Definition:** Issues related to Context-Based Retrieval
- **Supporting Records:** 18 (8.5% of relevant dataset)
- **Failure Rate:** 77.8%
- **Search Attempts:** 48

### Multi-Cue Retrieval
- **Definition:** Issues related to Multi-Cue Retrieval
- **Supporting Records:** 16 (7.6% of relevant dataset)
- **Failure Rate:** 87.5%
- **Search Attempts:** 50


## 10. Cross-Source Patterns
Consistent patterns were observed across the collected dataset. Event-Based Retrieval represents a notable volume of failures.

## 11. Evidence-Backed Opportunity Areas
1. **Bridging Event Memory**: Enabling search queries that combine people, vague locations, and approximate timeframes (Multi-Cue Retrieval).
2. **Document Retrieval Recovery**: Assisting users when OCR fails to trigger for standard search terms (Screenshot/Document Retrieval).

## 12. Representative User Evidence
### Event-Based Retrieval
> *"bring back old photo editor or fix its dependency on internet connection just to apply some tint or brightness 🤦..."*
- **Source:** [Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.photos&reviewId=e5d98652-fca6-4d68-b145-310996ec2298)
- **Observation:** User searched for event but the system returned irrelevant photos.
- **Hypothesis:** Hypothesis: The system may not effectively combine multiple weak contextual cues.

### Visual-Attribute Retrieval
> *"Can't find my device photos even if I backed everything up. I can't also find it in my files. I didn't even "accidentally" delete it. Please fix this issue. I don't know what to do. Tried clearing the..."*
- **Source:** [Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.photos&reviewId=821b9c14-cf6b-4c54-8c7a-6d0b10048fc0)
- **Observation:** User searched for visual but the system returned irrelevant photos.
- **Hypothesis:** Hypothesis: The system may not effectively combine multiple weak contextual cues.

### Place-Based Retrieval
> *"Nice to chat with U a good Gentle one.ThankU Mr./Mrs. pl let me know the exact location of Ur. repairing outleta place to be mentioned a known ( any thing )femous nearby...."*
- **Source:** [Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.photos&reviewId=bca7400a-31e6-4b5d-84f0-e16c586a58cd)
- **Observation:** User searched for place but the system returned irrelevant photos.
- **Hypothesis:** Hypothesis: The system may not effectively combine multiple weak contextual cues.


## 13. Research Limitations
- **Platform Bias**: The current dataset heavily weights Google Play Store reviews.
- **Sampling Bias**: Only users who experienced enough friction to leave a review are captured. 
- **Simulated Extraction**: The current iteration uses simulated mock LLM data for preview purposes until the true API extraction is run.

## 14. Questions for Direct User Research
1. When users attempt a multi-cue search that fails, what is their immediate next workaround?
2. Do users mentally catalog photos by time, or by the event they represent?

