from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    aws_glue as glue,
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

        # 👤 Reference existing SageMaker execution role
        role = iam.Role.from_role_name(self, "ExistingSageMakerRole", "unemployment-ml-sagemaker-role")

        CfnOutput(self, "SageMakerExecutionRoleArn", value=role.role_arn)

        # 📦 Model artifact location from SageMaker training job
        model_data_url = "s3://unemployment-ml-processed-data/model-artifacts/pipelines-908jgu1dn7xz-UnemploymentMLTraini-eyv470hBI9/output/model.tar.gz"

        # 📦 SageMaker model
        model = sagemaker.CfnModel(self, "XGBoostModel",
                                   execution_role_arn=role.role_arn,
                                   primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                                       image="683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.5-1",
                                       model_data_url=model_data_url
                                   ))

        # 📦 Endpoint config
        endpoint_config = sagemaker.CfnEndpointConfig(self, "EndpointConfig",
                                                      production_variants=[
                                                          sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                                                              initial_instance_count=1,
                                                              instance_type="ml.m5.large",
                                                              model_name=model.attr_model_name,
                                                              variant_name="AllTraffic"
                                                          )
                                                      ])

        # 📦 Endpoint
        sagemaker.CfnEndpoint(self, "SageMakerEndpoint",
                              endpoint_config_name=endpoint_config.attr_endpoint_config_name)

        # 📚 Glue Database
        database = glue.CfnDatabase(self, "UnemploymentDatabase",
                                    catalog_id=self.account,
                                    database_input=glue.CfnDatabase.DatabaseInputProperty(
                                        name="unemployment_data"
                                    ))

        # 📖 Glue Table for processed unemployment data
        glue.CfnTable(self, "ProcessedDataTable",
                      catalog_id=self.account,
                      database_name=database.ref,
                      table_input=glue.CfnTable.TableInputProperty(
                          name="processed_unemployment_data",
                          table_type="EXTERNAL_TABLE",
                          parameters={"classification": "csv"},
                          storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                              columns=[
                                  {"name": "unemployment_rate", "type": "double"},
                                  {"name": "year", "type": "int"},
                                  {"name": "month", "type": "int"},
                                  {"name": "quarter", "type": "int"}
                              ],
                              location=f"s3://{processed_bucket.bucket_name}/processed/",
                              input_format="org.apache.hadoop.mapred.TextInputFormat",
                              output_format="org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                              serde_info=glue.CfnTable.SerdeInfoProperty(
                                  serialization_library="org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
                                  parameters={"separatorChar": ","}
                              )
                          )
                      ))

        CfnOutput(self, "GlueDatabaseName", value=database.ref)


