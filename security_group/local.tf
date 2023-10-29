locals {
  vpc_id   = data.terraform_remote_state.network.outputs.vpc_id
  vpc_cidr = data.terraform_remote_state.network.outputs.vpc_cidr_block
  cluster_security_group_rules = {
    ingress_nodes_all = {
      description = "Node groups to cluster API"
      protocol    = "-1"
      from_port   = 1
      to_port     = 65535
      type        = "ingress"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress_node_all = {
      description = "Cluster API to node groups"
      protocol    = "-1"
      from_port   = 1
      to_port     = 65535
      type        = "egress"
      self        = true
    }
  }

  tags = {
    "kubernetes.io/cluster/demo" = "owned"
    Name                         = "eks-cluster-sg-demo"
  }
}