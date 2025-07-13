import boto3
from pipelines.pipeline import create_pipeline

# Configuration
role_arn = "arn:aws:iam::887290441850:role/unemployment-ml-sagemaker-role"
pipeline_name = "UnemploymentMLPipeline"

# Create pipeline instance
pipeline = create_pipeline(role_arn)

# Clean up any existing pipeline
try:
    pipeline.delete()
    print(f"Deleted existing pipeline: {pipeline_name}")
except Exception as e:
    print(f"No existing pipeline to delete: {str(e)}")

# Create and start pipeline
try:
    pipeline.upsert(role_arn=role_arn)
    execution = pipeline.start()
    print(f"✅ Pipeline execution started: {execution.arn}")
    print(f"Monitor at: https://console.aws.amazon.com/sagemaker/home?region={boto3.session.Session().region_name}#/pipelines/{pipeline_name}")
except Exception as e:
    print(f"❌ Pipeline failed: {str(e)}")
    raise
