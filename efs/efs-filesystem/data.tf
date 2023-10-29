data "terraform_remote_state" "network" {
  backend = "local"
  config = {
    path = "../../security_group/terraform.tfstate"
  }
}

data "aws_eks_cluster" "this" {
  name = "demo"
}

data "aws_eks_cluster_auth" "cluster" {
  name = data.aws_eks_cluster.this.name
}