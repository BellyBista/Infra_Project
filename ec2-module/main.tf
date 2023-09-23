resource "aws_instance" "ec2" {
  ami           = data.aws_ami.amzlinux2.id
  instance_type = var.my_instance_type
  vpc_id        = data.terraform_remote_state.vpc.outputs.vpc_id

  tags = {
    "Name" = var.name
  }
}