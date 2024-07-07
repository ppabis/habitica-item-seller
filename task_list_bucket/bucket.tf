provider "aws" { region = "eu-west-1" }

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "random_string" "suffix" {
  special = false
  upper   = false
  length  = 8
}

resource "aws_s3_bucket" "task_list_bucket" {
  bucket = "habitica-tasks-${random_string.suffix.result}"
}

output "bucket" { value = aws_s3_bucket.task_list_bucket.bucket }
