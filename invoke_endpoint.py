import boto3
import json

# --- Configuration ---
endpoint_name = "SageMakerEndpoint-asoVlzNljgal"
region_name = "us-east-1" # Make sure this matches your deployed region

# --- Initialize SageMaker Runtime client ---
runtime_client = boto3.client('sagemaker-runtime', region_name=region_name)

# --- Prepare your input data ---
# Your model was trained on data with 'Year', 'Month', 'Quarter' as features
# and 'UnemploymentRate' as the target.
# For inference, you provide the features to get a predicted UnemploymentRate.
# The 'preprocess.py' outputs CSV without headers, so the model expects raw CSV.

# Example: Data for a hypothetical prediction
# Let's say you want to predict for Year: 2025, Month: 7, Quarter: 3
# Provide these values as a comma-separated string.
# Make sure the number of values matches the number of features your model was trained on.
input_features = "2025,7,3"

# Content-Type for XGBoost models typically expects 'text/csv'
# if the input to training was CSV.
content_type = 'text/csv'
payload = input_features.encode('utf-8') # Encode the string to bytes

# --- Invoke the endpoint ---
print(f"Invoking endpoint: {endpoint_name} with payload: '{input_features}'")
try:
    response = runtime_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType=content_type,
        Body=payload
    )

    # Read and decode the response
    # The output from XGBoost is usually a single float representing the prediction
    result = response['Body'].read().decode('utf-8')

    print("\n--- Prediction Result ---")
    print(f"Predicted Unemployment Rate: {result}")
    print("-------------------------")

except Exception as e:
    print(f"\n--- ERROR invoking endpoint ---")
    print(f"Error: {e}")
    print("Please check: ")
    print("  1. Endpoint name is correct.")
    print("  2. Region is correct.")
    print("  3. Input data format (features count and order) matches your model's expectation.")
    print("  4. ContentType ('text/csv' is common for XGBoost).")
    print("  5. Your AWS credentials are configured correctly.")
    print("-----------------------------")

