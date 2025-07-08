variable "unemployment_ml" {
  description = "Project identifier"
  type        = string
  default     = "unemployment-ml"
}

variable "model_data_url" {
  type        = string
  description = "S3 URI of the trained model artifact .tar.gz"
  default     = ""
}

variable "create_model" {
  type        = bool
  description = "Whether to create the SageMaker model resource"
  default     = true
}