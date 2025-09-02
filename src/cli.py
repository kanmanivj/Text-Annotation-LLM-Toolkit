# src/cli.py
import argparse
from src.annotator import annotate_file
from src.evaluator import evaluate_file

def main():
    parser = argparse.ArgumentParser(description="Text Annotation & LLM Evaluation CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Annotate command
    annotate_parser = subparsers.add_parser("annotate")
    annotate_parser.add_argument("--input", required=True, help="Input JSON file")
    annotate_parser.add_argument("--output", required=True, help="Output JSON file")
    annotate_parser.add_argument("--label", default="general", help="Annotation label")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate")
    eval_parser.add_argument("--pred", required=True, help="Predictions JSON file")
    eval_parser.add_argument("--ref", required=True, help="Reference JSON file")

    args = parser.parse_args()

    if args.command == "annotate":
        result = annotate_file(args.input, args.output, args.label)
        print(f"Annotated {len(result)} texts.")
    elif args.command == "evaluate":
        report = evaluate_file(args.pred, args.ref)
        print(f"Evaluation Report: {report}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
