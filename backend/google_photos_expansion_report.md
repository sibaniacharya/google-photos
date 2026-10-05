# Google Photos Corpus Expansion Report

- **Original verified record count (from `real_data.json`):** 300
- **Newly collected record count:** 1722
- **Total unique Google Photos records available:** 2022
- **Source/Platform breakdown:** 100% Google Play Store (`com.google.android.apps.photos`)
- **Date-range coverage:** Included dynamically based on Sort.NEWEST order.
- **Duplicate count (skipped):** 278
- **Records rejected as non-Google-Photos (or low quality/no keyword):** 22000
- **Collection limitations:** Relied on `google-play-scraper` pagination which may cap out at ~10,000-20,000 reviews. Keyword filtering was applied to ensure the pool is dense with potential search/memory/retrieval complaints rather than just "good app" or "crashing" reviews.
- **Exact provenance:** Scraped directly from Google Play public reviews endpoint for app ID `com.google.android.apps.photos`, retaining original review IDs, timestamps, and ratings.
