import unittest
from ai_engine.validator import Validator
from ai_engine.config import load_config
from ai_engine.gemini_provider import GeminiProvider
from ai_engine.provider_base import APIErrorClassification
import json

class TestAIEngine(unittest.TestCase):
    def test_schema_validation(self):
        # We assume pydantic handles validation, this is a basic sanity check
        from ai_engine.schemas import ExtractedRecord
        data = {
            "record_id": "test_1",
            "target_problem_relevant": True,
            "retrieval_issue_type": "INCOMPLETE_MEMORY_RETRIEVAL",
            "problem_layer": "MEMORY_GAP",
            "retrieval_intent": "find dog",
            "target_object": "PHOTO",
            "memory_trigger": "UNKNOWN",
            "remembered_information": "UNKNOWN",
            "forgotten_or_unknown_information": "UNKNOWN",
            "search_strategy": "UNKNOWN",
            "attempts_or_workarounds": "UNKNOWN",
            "outcome": "FAILURE",
            "retrieval_category": "UNKNOWN",
            "underlying_need": "UNKNOWN",
            "memory_to_search_gap": "UNKNOWN",
            "evidence_quote": "missing dog photo",
            "confidence": "HIGH",
            "evidence_vs_hypothesis": "EVIDENCE"
        }
        rec = ExtractedRecord(**data)
        self.assertEqual(rec.record_id, "test_1")

    def test_evidence_quote_validation(self):
        val = Validator()
        extracted = [{"record_id": "1", "evidence_quote": "dog", "review_text": "cat", "source_url": "http"}]
        orig = {"1": {"record_id": "1", "review_text": "cat", "source_url": "http"}}
        errors = val.check_quality(extracted, orig)
        self.assertTrue(any("Evidence quote not found" in e for e in errors))

    def test_duplicate_record_detection(self):
        val = Validator()
        extracted = [{"record_id": "1"}, {"record_id": "1"}]
        orig = {"1": {}}
        errors = val.check_quality(extracted, orig)
        self.assertTrue(any("Duplicate record_ids" in e for e in errors))

    def test_original_review_preservation(self):
        val = Validator()
        extracted = [{"record_id": "1", "review_text": "changed", "source_url": "http"}]
        orig = {"1": {"record_id": "1", "review_text": "cat", "source_url": "http"}}
        errors = val.check_quality(extracted, orig)
        self.assertTrue(any("Original review_text or source_url was changed" in e for e in errors))

    def test_configuration_loading(self):
        conf = load_config()
        self.assertIn("AI_PROVIDER", conf)
        self.assertIn("AI_MODEL", conf)

    def test_provider_selection(self):
        # Without executing API
        provider = GeminiProvider("gemini-3.5-flash", "fake-key")
        self.assertEqual(provider.model_name, "gemini-3.5-flash")

    def test_quota_error_classification(self):
        provider = GeminiProvider("gemini", "fake")
        err = provider.classify_error(Exception("429 limit: 0"))
        self.assertTrue(err.is_quota_exhausted)
        self.assertTrue(err.is_rate_limit)
        
        err2 = provider.classify_error(Exception("503 UNAVAILABLE"))
        self.assertTrue(err2.is_temporary_server_error)

if __name__ == "__main__":
    unittest.main()
