import boto3
import json

runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")

endpoint_name = "unemployment-xgboost-endpoint"

# 📝 List of feature vectors: [Year, Month, Quarter, Region_Code]
payloads = [
    "2025,7,3,25",
    "2025,8,3,25",
    "2025,9,3,25",
    "2025,10,4,25",
    "2026,1,1,25"
]

for payload in payloads:
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Body=payload
    )

    result = json.loads(response["Body"].read().decode())
    print(f"Prediction for {payload}: {result}")

