output "bucket_name" {
  value = aws_s3_bucket.static_website.bucket
}

output "website_endpoint" {
  value = aws_s3_bucket.static_website.website_endpoint
}
