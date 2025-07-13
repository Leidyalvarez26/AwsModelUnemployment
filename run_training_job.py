import boto3
import time
from botocore.exceptions import ClientError

# 📦 Initialize SageMaker client
sagemaker = boto3.client('sagemaker', region_name='us-east-1')

# 📌 Generate unique job name with timestamp
job_name = 'unemployment-xgboost-train-' + str(int(time.time()))

# ✅ SageMaker execution role ARN (must match role created by CDK)
role_arn = 'arn:aws:iam::887290441850:role/unemployment-ml-sagemaker-role'

# ✅ S3 paths for input and output data
input_s3_uri = 's3://unemployment-ml-processed-data/sagemaker_input_data.csv'
output_s3_uri = 's3://unemployment-ml-processed-data/model-artifacts/'

try:
    response = sagemaker.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': '811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest',
            'TrainingInputMode': 'File'
        },
        RoleArn=role_arn,
        InputDataConfig=[
            {
                'ChannelName': 'train',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': input_s3_uri,
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'ContentType': 'text/csv'
            }
        ],
        OutputDataConfig={
            'S3OutputPath': output_s3_uri
        },
        ResourceConfig={
            'InstanceType': 'ml.m5.large',
            'InstanceCount': 1,
            'VolumeSizeInGB': 10
        },
        StoppingCondition={
            'MaxRuntimeInSeconds': 3600
        },
        HyperParameters={
            'objective': 'reg:linear',
            'num_round': '100',
            'max_depth': '5',
            'eta': '0.2',
            'subsample': '0.8',
            'min_child_weight': '3',
            'verbosity': '1'
        }
    )

    print(f"✅ Training job launched: {job_name}")

except ClientError as e:
    print("❌ Failed to create training job:")
    print(e.response['Error']['Message'])
