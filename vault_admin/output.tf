output "backend" {
  value = vault_aws_secret_backend_role.ec2-admin.backend

}

output "role" {
  value = vault_aws_secret_backend_role.ec2-admin.name

}