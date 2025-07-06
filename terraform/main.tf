# 📦 S3 Bucket for raw data
resource "aws_s3_bucket" "raw_data_bucket" {
  bucket        = "${var.unemployment-ml}-raw-data"
  force_destroy = true
}

# 📦 S3 Bucket for processed data
resource "aws_s3_bucket" "processed_data_bucket" {
  bucket        = "${var.unemployment-ml}-processed-data"
  force_destroy = true
}

# 👤 IAM Role for SageMaker
resource "aws_iam_role" "sagemaker_execution_role" {
  name               = "${var.unemployment-ml}-sagemaker-role"
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

