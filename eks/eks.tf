module "eks-user" {
  source    = "git::https://github.com/BellyBista/eks-user.git"
  developer = var.developer
  admin     = var.admin
}

resource "aws_eks_cluster" "demo" {
  name     = "demo"
  role_arn = data.terraform_remote_state.network.outputs.cluster_role

  vpc_config {
    subnet_ids = [
      data.terraform_remote_state.network.outputs.public[0], data.terraform_remote_state.network.outputs.public[1],
      data.terraform_remote_state.network.outputs.private[0], data.terraform_remote_state.network.outputs.private[1]
    ]
  }
}