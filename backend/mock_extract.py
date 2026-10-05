import json
import random
from schema import ExtractedInsight, ConfidenceLevel, MemorySearchGap, Evidence

def generate_mock_extraction(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    insights = []
    
    categories_pool = [
        "Event-Based Retrieval", "Context-Based Retrieval", "Place-Based Retrieval",
        "Person-Based Retrieval", "Time-Based Retrieval", "Visual-Attribute Retrieval",
        "Object-Based Retrieval", "Screenshot / Document Retrieval", "Multi-Cue Retrieval"
    ]
    
    memory_cues_pool = ["event", "place", "person", "time", "visual appearance", "object", "context"]
    forgotten_pool = ["exact date", "exact location", "filename", "exact words in image", "person's name"]
    outcomes = ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "ABANDONED"]
    
    for record in raw_data:
        # Determine if relevant
        is_relevant = random.random() > 0.3 # 70% chance of being relevant since we filtered by keywords
        
        insight = {
            "record_id": record["record_id"],
            "source": record["source"],
            "source_url": record["source_url"],
            "original_text": record["text"],
            "is_retrieval_relevant": is_relevant,
            "relevance_confidence": {"level": "HIGH", "reason": "Mentions search keywords clearly."},
            "relevance_reason": "User describes trying to find a photo.",
        }
        
        if is_relevant:
            cat = random.choice(categories_pool)
            insight.update({
                "retrieval_intent": "photo",
                "memory_trigger": "needed something",
                "remembered_information": random.sample(memory_cues_pool, k=random.randint(1, 3)),
                "forgotten_information": random.sample(forgotten_pool, k=random.randint(1, 2)),
                "search_formulation": ["mock search term"],
                "search_classification": ["keyword", "natural language"][:random.randint(1, 2)],
                "retrieval_attempts": random.randint(1, 5),
                "workaround_used": random.choice([True, False]),
                "retrieval_outcome": random.choices(outcomes, weights=[10, 20, 50, 20])[0], # Skew towards failure
                "primary_failure_reason": random.choice(["Missing exact keywords", "Missing date", "Context not searchable", "OCR/text retrieval failure"]),
                "retrieval_categories": [cat],
                "memory_search_gap": {
                    "what_user_remembers": ["mock remember event/place"],
                    "what_user_forgot": ["mock forgot date/location"],
                    "what_user_searches": ["mock search keyword"],
                    "what_result_they_get": "FAILURE",
                    "where_the_gap_occurs_observed": f"User searched for {cat.split('-')[0].lower()} but the system returned irrelevant photos.",
                    "where_the_gap_occurs_hypothesis": f"Hypothesis: The system may not effectively combine multiple weak contextual cues."
                },
                "underlying_need_observed": "Search using approximate memories.",
                "underlying_need_hypothesis": "The system cannot map episodic memory to metadata."
            })
            
        insights.append(insight)
        
    final_output = {"insights": insights}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)
        
    print(f"Mock extracted {len(insights)} records to {output_file}")

if __name__ == "__main__":
    generate_mock_extraction("real_data.json", "extracted_records.json")
