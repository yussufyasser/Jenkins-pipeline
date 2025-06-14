 terraform {
  backend "s3" {
    bucket         = "sign-recognition-app-state"
    key            = "eks/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks-sign-recognition"
    encrypt        = true
  }
}

