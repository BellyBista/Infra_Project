data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "bootcamp32-dev-47"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}