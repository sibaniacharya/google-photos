import argparse
from ai_engine.extractor import ExtractorEngine

def main():
    parser = argparse.ArgumentParser(description="AI Discovery Engine Extraction")
    parser.add_argument("--dry-run", action="store_true", help="Validate pipeline without calling APIs")
    args = parser.parse_args()

    input_file = "backend/gemini_candidate_sample.json"
    output_file = "backend/gemini_extracted_candidate_sample.json"
    report_file = "backend/gemini_extraction_report.md"

    engine = ExtractorEngine(dry_run=args.dry_run)
    engine.run(input_file, output_file, report_file)

if __name__ == "__main__":
    main()
