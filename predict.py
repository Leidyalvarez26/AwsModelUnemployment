import boto3
import json

# Update with your endpoint name
endpoint_name = 'unemployment-xgboost-endpoint'

# Sample data — same order and type as your training CSV columns:
# ['Unemployment Rate', 'Year', 'Month', 'Quarter', 'Region Code']
payload = '2025,7,3,25'  # Example: predicting based on those inputs

# Create SageMaker runtime client
runtime = boto3.client('sagemaker-runtime', region_name='us-east-1')

# Invoke endpoint
response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='text/csv',
    Body=payload
)

# Decode result
result = response['Body'].read().decode('utf-8')
print("✅ Prediction result:", result)
