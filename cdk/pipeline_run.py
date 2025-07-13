from pipelines.pipeline import create_pipeline
import boto3

role_arn = "arn:aws:iam::887290441850:role/unemployment-ml-sagemaker-role"
pipeline = create_pipeline(role_arn)

# Submit pipeline
pipeline.upsert(role_arn)
execution = pipeline.start()
print("✅ Pipeline execution started:", execution.arn)
