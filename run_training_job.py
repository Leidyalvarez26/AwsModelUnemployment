import boto3
import time

sagemaker = boto3.client('sagemaker', region_name='us-east-1')

job_name = 'unemployment-xgboost-train-' + str(int(time.time()))

response = sagemaker.create_training_job(
    TrainingJobName=job_name,
    AlgorithmSpecification={
        'TrainingImage': '811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest',
        'TrainingInputMode': 'File'
    },
    RoleArn='arn:aws:iam::887290441850:role/unemployment-ml-sagemaker-role',
    InputDataConfig=[
        {
            'ChannelName': 'train',
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': 's3://unemployment-ml-processed-data/sagemaker_input_data.csv',
                    'S3DataDistributionType': 'FullyReplicated'
                }
            },
            'ContentType': 'text/csv'
        }
    ],
    OutputDataConfig={
        'S3OutputPath': 's3://unemployment-ml-processed-data/model-artifacts/'
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

print("✅ Training job launched:", job_name)
