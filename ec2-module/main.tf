resource "aws_instance" "ec2" {
  ami           = data.aws_ami.amzlinux2.id
  instance_type = var.my_instance_type
  monitoring    = true
  ebs_optimized = true
  metadata_options {
    http_endpoint = "disabled"
    http_tokens   = "required"
  }
  root_block_device {
    encrypted = true
  }
  iam_instance_profile = "test"

  credit_specification {
    cpu_credits = "unlimited"
  }


  tags = {
    "Name" = var.name
  }
}

resource "aws_launch_configuration" "ec2" {
  instance_type = var.my_instance_type
  image_id      = data.aws_ami.amzlinux2.id
  root_block_device {
    encrypted = true
  }
  metadata_options {
    http_endpoint = "disabled"
    http_tokens   = "required"
  }

}
