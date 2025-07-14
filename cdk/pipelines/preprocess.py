import pandas as pd
import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()
    
    try:
        # Verify input exists
        if not os.path.exists(args.input_path):
            raise FileNotFoundError(f"Input file not found at {args.input_path}")
        print(f"Processing file: {args.input_path}")

        # Load data
        df = pd.read_csv(args.input_path, header=None)
        df.columns = ["UnemploymentRate", "Year", "Month", "Quarter"]

        # Drop missing
        df.dropna(inplace=True)

        # Drop the target (UnemploymentRate) for training input
        df_features = df[["Year", "Month", "Quarter"]]

        # Ensure output directory exists
        os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

        # Write features-only CSV to output
        df_features.to_csv(args.output_path, index=False, header=False)
        print(f"Successfully wrote output to {args.output_path}")

    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()


