packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1"
    }
  }
}

variable "ami_name" {
  type = string
  #default = "bootcamp32-g09-prod"
}

source "amazon-ebs" "ubuntu" {
  instance_type = "t2.micro"
  ami_name      = var.ami_name
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

build {
  name = "docker-test-packer"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]
  provisioner "shell" {
    script = "/Users/quadribello/Infra_Project/ami_packer/ansible.sh"
  }
  provisioner "ansible-local" {
    playbook_file = "/Users/quadribello/Infra_Project/ami_packer/docker.yml"
  }
}