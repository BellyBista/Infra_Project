output "efs_sg" {
  value = aws_security_group.allow_nfs.id
}