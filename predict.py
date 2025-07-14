import boto3
import argparse

# Initialize runtime client
runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help="Comma-separated CSV values for prediction (e.g. '2025,7,3')")
args = parser.parse_args()

input_data = args.input

# Validate input length (3 features expected)
if len(input_data.split(",")) != 3:
    print(f"❌ Expected 3 values, got {len(input_data.split(','))}")
    exit(1)

# Replace this with your deployed endpoint name
endpoint_name = "SageMakerEndpoint-j7lFiQe4UebR"

# Invoke endpoint
try:
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='text/csv',
        Body=input_data
    )
    result = response['Body'].read().decode('utf-8')
    print(f"✅ Predicted result: {result}")

except Exception as e:
    print(f"❌ Error during prediction: {e}")

