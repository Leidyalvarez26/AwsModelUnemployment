from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    RemovalPolicy,
    CfnOutput as CfnOutput
)
from constructs import Construct


class UnemploymentMLStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 📦 Raw data bucket
        raw_bucket = s3.Bucket(self, "RawDataBucket",
                               removal_policy=RemovalPolicy.DESTROY)

        # 📦 Processed data bucket
        processed_bucket = s3.Bucket(self, "ProcessedDataBucket",
                                     removal_policy=RemovalPolicy.DESTROY)

        # 👤 Reference existing SageMaker execution role (manually created)
        role = iam.Role.from_role_name(self, "ExistingSageMakerRole", "unemployment-ml-sagemaker-role")

        # Expose role ARN
        CfnOutput(self, "SageMakerExecutionRoleArn", value=role.role_arn)

        # 📦 Define model artifact location (use your real training job path here)
        model_data_url="s3://unemployment-ml-processed-data/model-artifacts/unemployment-xgboost-train-1752372725/output/model.tar.gz"

        # 📦 SageMaker model
        model = sagemaker.CfnModel(self, "XGBoostModel",
                                   execution_role_arn=role.role_arn,
                                   primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                                       image="811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest",
                                       model_data_url=model_data_url
                                   ))

        # 📦 Endpoint config
        endpoint_config = sagemaker.CfnEndpointConfig(self, "EndpointConfig",
                                                      production_variants=[
                                                          sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                                                              initial_instance_count=1,
                                                              instance_type="ml.t2.medium",
                                                              model_name=model.attr_model_name,
                                                              variant_name="AllTraffic"
                                                          )
                                                      ])

        # 📦 Endpoint
        sagemaker.CfnEndpoint(self, "SageMakerEndpoint",
                              endpoint_config_name=endpoint_config.attr_endpoint_config_name)

