import boto3

endpoint_name = "SageMakerEndpoint-asoVIzNLjgal"  # replace if needed

sagemaker_runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")

payload = "2025,6,2\n" 

response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="text/csv",
    Body=payload
)

result = response['Body'].read().decode('utf-8')
print("Predicted result:", result)
