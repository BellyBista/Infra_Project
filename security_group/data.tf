data "terraform_remote_state" "network" {
  backend = "local"
  config = {
    path = "../vpc-eks/terraform.tfstate"
  }
}

data "aws_eks_cluster" "this" {
  name = "demo"
}

data "aws_security_group" "cluster" {
  id = data.aws_eks_cluster.this.vpc_config[0].cluster_security_group_id
}