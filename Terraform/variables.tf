variable "aws_region" {
    type = string
    default = "us-east-1"
  
}

variable "az" {
    type = list(string)
    default = ["us-east-1a", "us-east-1b"]
  
}

variable "cluster_name" {
    type = string
    default = "my-sign-recognition-cluster"
  
}