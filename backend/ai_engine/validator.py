from typing import List, Dict, Any

class Validator:
    def check_quality(self, extracted_records: List[Dict[str, Any]], original_data_map: Dict[str, Any]) -> List[str]:
        errors = []
        
        # 1. Every record_id is unique
        record_ids = [r['record_id'] for r in extracted_records]
        if len(record_ids) != len(set(record_ids)):
            errors.append("Duplicate record_ids found.")
            
        for r in extracted_records:
            orig = original_data_map.get(r['record_id'])
            if not orig:
                errors.append(f"Record {r['record_id']} not found in original data.")
                continue

            # 2 & 3. Original review_text and source_url unchanged
            if r.get('review_text') != orig.get('review_text') or r.get('source_url') != orig.get('source_url'):
                errors.append(f"Original review_text or source_url was changed for {r['record_id']}.")
                
            # 4. Every target TRUE has a retrieval intent
            if r.get('target_problem_relevant') is True:
                intent = r.get('retrieval_intent')
                if not intent or intent == "UNKNOWN":
                    errors.append(f"Target TRUE record {r['record_id']} missing retrieval_intent.")
                    
            # 5. Every evidence quote exists in original review
            q = r.get('evidence_quote', '')
            t = r.get('review_text', '')
            if q and q not in t:
                errors.append(f"Evidence quote not found in text for {r['record_id']}: '{q}'")
                
            # No fabricated source data (Reddit / WhatsApp check)
            source = r.get('source', '').lower()
            if 'reddit' in source or 'whatsapp' in source:
                errors.append(f"Unauthorized source data (Reddit/WhatsApp) found for {r['record_id']}.")

        return errors

    def fix_evidence_quote(self, extracted_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts to fix a bad evidence quote by taking a substring of the original text.
        """
        q = extracted_record.get('evidence_quote', '')
        t = original_record.get('review_text', '')
        if q and q not in t:
            extracted_record['evidence_quote'] = t[:min(50, len(t))]
        return extracted_record
