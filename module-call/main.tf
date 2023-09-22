/*
module "s3" {
  source = "git::https://github.com/quadribello/Infra_Project.git//s3-module?ref=v1.0.2"
  region = "us-east-1"
  env = "development"
}
*/

module "ec2" {
  source = "git::https://github.com/quadribello/Infra_Project.git//ec2-module?ref=v1.3.0"
  my_instance_type = "t2.micro"
  name = "dev_ec2"
  region = "us-east-1"
}