import argparse
from mlops_pipeline.data import read_csv_file
from mlops_pipeline.model import run_predictions
from mlops_pipeline.monitor import run_monitoring


def main():
    parser = argparse.ArgumentParser(description="MLOps Pipeline Runner")
    subparsers = parser.add_subparsers(dest="command", help="Choose an operation")

    # Inference command
    parser_infer = subparsers.add_parser("inference", help="Run inference on a dataset")
    parser_infer.add_argument("--data", required=True, help="Path to input dataset")

    # Monitoring command
    parser_monitor = subparsers.add_parser("monitoring", help="Run monitoring on outputs")
    parser_monitor.add_argument("--output_dir", required=True, help="Path to output directory")
    parser_monitor.add_argument("--truth_dir", required=True, help="Path to truth directory")

    args = parser.parse_args()

    if args.command == "inference":
        data = read_csv_file(args.data)
        predictions = run_predictions(data)
        print(f"Inference results: {predictions}")
    elif args.command == "monitoring":
        run_monitoring(args.output_dir, args.truth_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()