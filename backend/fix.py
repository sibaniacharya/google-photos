import json
import os

with open('backend/real_data.json', 'r', encoding='utf-8') as f:
    real_data = json.load(f)

existing_urls = {r.get('source_url') for r in real_data}

with open('backend/google_photos_expanded.json', 'r', encoding='utf-8') as f:
    expanded_data = json.load(f)

new_data = []
duplicates = 0
for r in expanded_data:
    if r.get('source_url') in existing_urls:
        duplicates += 1
    else:
        new_data.append(r)

with open('backend/google_photos_expanded.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2)

with open('backend/google_photos_expansion_report.md', 'r', encoding='utf-8') as f:
    report = f.read()

report = report.replace('**Original verified record count (from `real_data.json`):** 0', f'**Original verified record count (from `real_data.json`):** {len(real_data)}')
report = report.replace('**Newly collected record count:** 2000', f'**Newly collected record count:** {len(new_data)}')
report = report.replace('**Total unique Google Photos records available:** 2000', f'**Total unique Google Photos records available:** {len(real_data) + len(new_data)}')
report = report.replace('**Duplicate count (skipped):** 0', f'**Duplicate count (skipped):** {duplicates}')

with open('backend/google_photos_expansion_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f'Deduplicated {duplicates} records. New count: {len(new_data)}')
