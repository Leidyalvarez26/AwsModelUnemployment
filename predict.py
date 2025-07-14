import boto3
import argparse
import sys

# 📦 Parse CLI arguments
parser = argparse.ArgumentParser(description="Invoke SageMaker endpoint for unemployment prediction.")
parser.add_argument("--endpoint-name", type=str, default="SageMakerEndpoint-iLsuBs92FvnF", help="SageMaker endpoint name")
parser.add_argument("--input", type=str, required=True, help="Comma-separated values to predict")

args = parser.parse_args()

# ✅ Validate input
input_values = args.input.split(",")
if not all(input_values):
    print("❌ Input values cannot be empty.")
    sys.exit(1)

# 📦 Initialize runtime client
runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')

try:
    response = runtime.invoke_endpoint(
        EndpointName=args.endpoint_name,
        ContentType='text/csv',
        Body=args.input
    )

    result = response['Body'].read().decode('utf-8')
    print(f"✅ Predicted result: {result}")

except Exception as e:
    print(f"❌ Error during prediction: {e}")
