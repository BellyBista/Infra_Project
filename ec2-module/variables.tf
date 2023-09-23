variable "my_instance_type" {
  type = string
  #default = "t2.micro"
}

variable "name" {
  type = string
  #default = "dev"
}

variable "region" {
  type = string
  #default = "us-east-1"
}

variable "instance_count" {
  description = "The number of EC2 instances to create"
  type        = number
}

variable "my_key" {
  type = string
}