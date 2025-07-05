output "raw_data_bucket" {
  value = aws_s3_bucket.raw_data_bucket.bucket
}

output "processed_data_bucket" {
  value = aws_s3_bucket.processed_data_bucket.bucket
}

output "sagemaker_execution_role_arn" {
  value = aws_iam_role.sagemaker_execution_role.arn
}
