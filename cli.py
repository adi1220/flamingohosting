#!/usr/bin/env python3
import argparse
import json
import sys
import os
from pathlib import Path
import audio_flamingo_runner as runner


def transcribe_command(args):
    """Handle transcribe command."""
    # Load model
    model_dir = args.model_dir or os.getenv("MODEL_DIR", "{{MODEL_DIR}}")
    print(f"Loading model from {model_dir}...", file=sys.stderr)
    model_bundle = runner.load_model(model_dir=model_dir)
    
    # Get file paths
    if args.path:
        paths = [args.path]
    elif args.paths:
        paths = args.paths
    else:
        print("Error: Must provide --path or --paths", file=sys.stderr)
        sys.exit(1)
    
    # Validate paths
    for path in paths:
        if not Path(path).exists():
            print(f"Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)
    
    # Run transcription
    if len(paths) == 1:
        print(f"Transcribing single file: {paths[0]}", file=sys.stderr)
        result = runner.transcribe_file(
            paths[0],
            model_bundle,
            args.prompt,
            args.max_new_tokens
        )
        results = [result]
    else:
        print(f"Transcribing {len(paths)} files...", file=sys.stderr)
        results = runner.transcribe_files(
            paths,
            model_bundle,
            args.prompt,
            args.max_new_tokens
        )
    
    # Output JSON
    output = {"results": results}
    print(json.dumps(output, indent=2))
    
    # Write to file
    output_file = args.output or "transcribe_results.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults written to {output_file}", file=sys.stderr)


def evaluate_command(args):
    """Handle evaluate command."""
    # Load model
    model_dir = args.model_dir or os.getenv("MODEL_DIR", "{{MODEL_DIR}}")
    print(f"Loading model from {model_dir}...", file=sys.stderr)
    model_bundle = runner.load_model(model_dir=model_dir)
    
    # Validate directories
    if not Path(args.audio_dir).exists():
        print(f"Error: Audio directory not found: {args.audio_dir}", file=sys.stderr)
        sys.exit(1)
    
    if not args.use_folder_as_label:
        if not args.gt_dir:
            print("Error: --gt-dir is required when not using --use-folder-as-label", file=sys.stderr)
            sys.exit(1)
        if not Path(args.gt_dir).exists():
            print(f"Error: Ground truth directory not found: {args.gt_dir}", file=sys.stderr)
            sys.exit(1)
    
    # Run evaluation
    if args.use_folder_as_label:
        print(f"Evaluating folder: {args.audio_dir} (using subfolder names as labels)", file=sys.stderr)
    else:
        print(f"Evaluating folder: {args.audio_dir}", file=sys.stderr)
    
    result = runner.evaluate_folder(
        args.audio_dir,
        args.gt_dir,
        model_bundle,
        args.prompt,
        args.max_new_tokens,
        args.match_mode,
        args.use_folder_as_label
    )
    
    # Output JSON
    print(json.dumps(result, indent=2))
    
    # Write to file
    output_file = args.output or "evaluation_results.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nResults written to {output_file}", file=sys.stderr)
    
    # Print summary
    summary = result['summary']
    print(f"\n=== Evaluation Summary ===", file=sys.stderr)
    print(f"Total files: {summary['count']}", file=sys.stderr)
    print(f"True Positives: {summary['tp']}", file=sys.stderr)
    print(f"False Positives: {summary['fp']}", file=sys.stderr)
    print(f"False Negatives: {summary['fn']}", file=sys.stderr)
    print(f"Precision: {summary['precision']:.4f}", file=sys.stderr)
    print(f"Recall: {summary['recall']:.4f}", file=sys.stderr)
    print(f"F1 Score: {summary['f1']:.4f}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Audio Flamingo CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        help="Path to model directory (default: $MODEL_DIR or {{MODEL_DIR}})"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser(
        "transcribe",
        help="Transcribe audio file(s)"
    )
    transcribe_parser.add_argument(
        "--path",
        type=str,
        help="Path to single audio file"
    )
    transcribe_parser.add_argument(
        "--paths",
        type=str,
        nargs="+",
        help="Paths to multiple audio files"
    )
    transcribe_parser.add_argument(
        "--prompt",
        type=str,
        help="Optional prompt for conditioning"
    )
    transcribe_parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=128,
        help="Maximum number of tokens to generate (default: 128)"
    )
    transcribe_parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file (default: transcribe_results.json)"
    )
    
    # Evaluate command
    evaluate_parser = subparsers.add_parser(
        "evaluate",
        help="Evaluate model on a folder"
    )
    evaluate_parser.add_argument(
        "--audio-dir",
        type=str,
        required=True,
        help="Directory containing audio files (or subdirectories with audio files)"
    )
    evaluate_parser.add_argument(
        "--gt-dir",
        type=str,
        help="Directory containing ground truth .txt files (not needed if using --use-folder-as-label)"
    )
    evaluate_parser.add_argument(
        "--use-folder-as-label",
        action="store_true",
        help="Use subfolder names as ground truth labels (e.g., audio_dir/piano/*.wav, audio_dir/guitar/*.wav)"
    )
    evaluate_parser.add_argument(
        "--prompt",
        type=str,
        help="Optional prompt for conditioning"
    )
    evaluate_parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=128,
        help="Maximum number of tokens to generate (default: 128)"
    )
    evaluate_parser.add_argument(
        "--match-mode",
        type=str,
        default="exact",
        choices=["exact", "contains"],
        help="Matching mode: 'exact' for exact match, 'contains' if GT is contained in prediction (default: exact)"
    )
    evaluate_parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file (default: evaluation_results.json)"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "transcribe":
        transcribe_command(args)
    elif args.command == "evaluate":
        evaluate_command(args)


if __name__ == "__main__":
    main()
