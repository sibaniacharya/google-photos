import json
import random

def create_sample():
    with open('backend/google_photos_expanded.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    potentially_relevant = []
    borderline = []
    negative_control = []
    
    retrieval_keywords = ['search', 'find', 'locate', 'look for', 'looking for', 'retrieve', 'fetch']
    object_keywords = ['photo', 'picture', 'pic', 'image', 'video', 'screenshot', 'document']
    memory_keywords = ['remember', 'forgot', 'forget', 'vague', 'memory', 'old', 'years ago', 'when', 'date', 'time', 'place', 'location', 'event']
    borderline_keywords = ['backup', 'sync', 'slow', 'metadata', 'tags', 'organize', 'album', 'folder', 'update', 'crash', 'feature', 'navigation']

    def check_signals(text):
        text_lower = text.lower()
        signals = []
        for kw in retrieval_keywords:
            if kw in text_lower: signals.append(kw)
        for kw in object_keywords:
            if kw in text_lower: signals.append(kw)
        for kw in memory_keywords:
            if kw in text_lower: signals.append(kw)
        for kw in borderline_keywords:
            if kw in text_lower: signals.append(kw)
        return list(set(signals))

    for rec in data:
        text = rec.get('review_text', '').lower()
        if not text:
            continue
            
        has_retrieval = any(kw in text for kw in retrieval_keywords)
        has_object = any(kw in text for kw in object_keywords)
        has_memory = any(kw in text for kw in memory_keywords)
        has_borderline = any(kw in text for kw in borderline_keywords)
        
        signals = check_signals(text)
        
        if has_retrieval and has_object and has_memory and len(text.split()) > 10:
            potentially_relevant.append((rec, signals))
        elif (has_retrieval or has_memory) and has_borderline and len(text.split()) > 10:
            borderline.append((rec, signals))
        elif not has_retrieval and not has_memory and len(text.split()) > 5:
            negative_control.append((rec, signals))
            
    # Sample
    random.seed(42)
    sample_relevant = random.sample(potentially_relevant, min(40, len(potentially_relevant)))
    sample_borderline = random.sample(borderline, min(20, len(borderline)))
    sample_negative = random.sample(negative_control, min(20, len(negative_control)))
    
    # Format output
    output_records = []
    
    def process_sample(sample_list, group_name):
        for rec, signals in sample_list:
            out_rec = {
                'record_id': rec.get('record_id'),
                'review_text': rec.get('review_text'),
                'source': rec.get('source'),
                'source_url': rec.get('source_url'),
                'review_date': rec.get('review_date'),
                'rating': rec.get('rating'),
                'selection_group': group_name,
                'selection_signals': signals
            }
            output_records.append(out_rec)
            
    process_sample(sample_relevant, 'POTENTIALLY_RELEVANT')
    process_sample(sample_borderline, 'BORDERLINE')
    process_sample(sample_negative, 'NEGATIVE_CONTROL')
    
    with open('backend/gemini_candidate_sample.json', 'w', encoding='utf-8') as f:
        json.dump(output_records, f, indent=2)
        
    # Generate report
    report = f"# Gemini Candidate Sample Report\n\n"
    report += f"1. **Source dataset count:** {len(data)}\n"
    report += f"2. **Number selected:** {len(output_records)}\n"
    report += f"3. **Potentially relevant count:** {len(sample_relevant)}\n"
    report += f"4. **Borderline count:** {len(sample_borderline)}\n"
    report += f"5. **Negative-control count:** {len(sample_negative)}\n"
    
    # Selection signals used
    all_signals_used = retrieval_keywords + object_keywords + memory_keywords + borderline_keywords
    report += f"6. **Selection signals used:** {', '.join(set(all_signals_used))}\n"
    
    # Signal distribution
    signal_counts = {}
    for rec in output_records:
        for s in rec['selection_signals']:
            signal_counts[s] = signal_counts.get(s, 0) + 1
            
    report += f"7. **Signal distribution:**\n"
    for s, c in sorted(signal_counts.items(), key=lambda x: -x[1]):
        report += f"   - {s}: {c}\n"
        
    report += f"\n8. **Representative selected records:**\n\n"
    rep_sample = random.sample(output_records, min(20, len(output_records)))
    for i, rec in enumerate(rep_sample):
        report += f"### Record {i+1} [{rec['selection_group']}]\n"
        report += f"- **ID:** {rec['record_id']}\n"
        report += f"- **Signals:** {', '.join(rec['selection_signals'])}\n"
        report += f"- **Text:** > {rec['review_text']}\n\n"
        
    report += f"9. **Limitations:**\n"
    report += f"- Semantic relevance has NOT yet been established. These are candidate records for Gemini extraction.\n"
    report += f"- Keyword-based selection is rudimentary and cannot understand the context or nuance of the review.\n"
    
    with open('backend/gemini_candidate_sample_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Sample generation complete: {len(output_records)} records selected.")
    print(f"Relevant: {len(sample_relevant)}, Borderline: {len(sample_borderline)}, Negative: {len(sample_negative)}")
    
if __name__ == '__main__':
    create_sample()
