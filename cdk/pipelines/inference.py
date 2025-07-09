import boto3

runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")
endpoint_name = "unemployment-xgboost-endpoint"

payloads = ["2025,7,3,25", "2025,8,3,25"]

for payload in payloads:
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Body=payload
    )
    result = response["Body"].read().decode()
    print(f"Prediction for {payload}: {result}")

