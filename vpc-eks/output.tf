output "private" {
  value = aws_subnet.private.*.id
}

output "public" {
  value = aws_subnet.public.*.id

}


output "node_role" {
  value = module.iam_role.node_role
}

output "cluster_role" {
  value = module.iam_role.cluster_role
}

output "developer_password" {
  value = module.eks-user.developer_password
}

output "admin_password" {
  value = module.eks-user.admin_password
}
