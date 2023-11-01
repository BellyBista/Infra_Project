# Infra_Project
Private repo for terraform modules created
This repo is connected to the terraform_workflows repo via ssh.

This repo contain a fully configured:
- eks cluster
- ec2-module and s3-module that passed the checkov test
- vpc module
- packer for ami
- vault admin for credential mangement 


### Sequence of runs of eks from provisioning to monitoring
This repo contain a fully configured eks cluster 

vpc-eks ---> eks ---> security_group ---> test-oidc ---> autoscaling ---> argocd ---> efs ---> istio