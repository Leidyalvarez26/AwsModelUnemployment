# 📦 S3 Bucket for raw data
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket        = "${var.unemployment_ml}-raw-data"
  force_destroy = true
}

# 📦 S3 Bucket for processed data
resource "aws_s3_bucket" "processed_data_bucket" {
  bucket        = "${var.unemployment_ml}-processed-data"
  force_destroy = true
}

# 👤 IAM Role for SageMaker
resource "aws_iam_role" "sagemaker_execution_role" {
  name               = "${var.unemployment_ml}-sagemaker-role"
  assume_role_policy = data.aws_iam_policy_document.sagemaker_assume_role_policy.json
}

# 📜 Trust policy for SageMaker
data "aws_iam_policy_document" "sagemaker_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}

# 📜 Inline policy to allow access to S3 and logs
resource "aws_iam_role_policy" "sagemaker_policy" {
  name   = "sagemaker-s3-policy"
  role   = aws_iam_role.sagemaker_execution_role.id
  policy = data.aws_iam_policy_document.sagemaker_policy.json
}

# 📜 IAM Policy for S3 + CloudWatch logs permissions
data "aws_iam_policy_document" "sagemaker_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.raw_data_bucket.arn,
      "${aws_s3_bucket.raw_data_bucket.arn}/*",
      aws_s3_bucket.processed_data_bucket.arn,
      "${aws_s3_bucket.processed_data_bucket.arn}/*"
    ]
  }

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }
}

# 📦 SageMaker model resource (conditional)
resource "aws_sagemaker_model" "unemployment_xgboost_model" {
  count              = var.create_model ? 1 : 0
  name               = "unemployment-xgboost-model"
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn

  primary_container {
    image           = "811284229777.dkr.ecr.us-east-1.amazonaws.com/xgboost:latest"
    model_data_url  = var.model_data_url
  }
}

# 📦 SageMaker endpoint config (conditional)
resource "aws_sagemaker_endpoint_configuration" "unemployment_endpoint_config" {
  count = var.create_model ? 1 : 0
  name  = "unemployment-xgboost-endpoint-config"

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.unemployment_xgboost_model[0].name
    initial_instance_count = 1
    instance_type          = "ml.t2.medium"
  }
}

# 📦 SageMaker endpoint (conditional)
resource "aws_sagemaker_endpoint" "unemployment_endpoint" {
  count                = var.create_model ? 1 : 0
  name                 = "unemployment-xgboost-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.unemployment_endpoint_config[0].name
}




