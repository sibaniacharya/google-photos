import json
data = json.load(open('backend/reclassified_records.json', encoding='utf-8'))
records = [r for r in data.get('insights', []) if r.get('target_problem_relevant')]
with open('temp_records.txt', 'w', encoding='utf-8') as f:
    for r in records:
        f.write(f"ID: {r.get('record_id')}\n")
        f.write(f"Text: {r.get('original_text', '')}\n")
        f.write(f"Remembers: {r.get('remembered_information')}\n")
        f.write(f"Forgot: {r.get('forgotten_information')}\n")
        f.write(f"Search: {r.get('search_formulation')}\n")
        f.write(f"Outcome: {r.get('retrieval_outcome')}\n")
        f.write(f"Failure Reason: {r.get('primary_failure_reason')}\n")
        f.write(f"Issue Type: {r.get('retrieval_issue_type')}\n")
        f.write(f"Layer: {r.get('problem_layer')}\n")
        f.write('-'*40 + '\n')
