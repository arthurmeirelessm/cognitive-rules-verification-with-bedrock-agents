variable "bucket_name" {
  type        = string
  description = "Nome do bucket S3 para o site estático"
}

variable "tags" {
  type        = map(string)
  description = "Tags aplicadas ao bucket"
  default     = {}
}
