# Infrastructure Project

This repository is a work in progress housing Terraform modules designed for various infrastructure components. The repository is linked to the `terraform_workflows` repository via SSH.

## Contents

This repository encompasses fully configured Terraform modules for:

- EKS cluster
- EC2 module and S3 module that have successfully passed the Checkov test
- VPC module
- Packer for creating Amazon Machine Images (AMI)
- Vault admin for credential management

## Sequence of Runs for EKS Setup and Monitoring

The following sequence outlines the steps involved in provisioning and monitoring the EKS cluster:

1. **VPC Setup (`vpc-eks`):**
   - Configuration of the Virtual Private Cloud (VPC) for EKS.

2. **EKS Cluster Setup (`eks`):**
   - Deployment of the EKS cluster.
   - Connection to EKS CNI (Container Network Interface) for both `eks-cni-cluster` and `eks-cni-node`.

3. **Security Group Configuration (`security_group`):**
   - Setup of security groups for controlling inbound and outbound traffic.

4. **Test OIDC (`test-oidc`):**
   - Verification of OpenID Connect (OIDC) authentication.

5. **Autoscaling (`autoscaling`):**
   - Implementation of autoscaling for managing cluster capacity.

6. **ArgoCD (`argocd`):**
   - Integration of ArgoCD for continuous delivery of Kubernetes applications.

7. **EFS (Elastic File System) Setup (`efs`):**
   - Configuration of EFS to provide scalable and elastic file storage.

8. **Istio (`istio`):**
   - Implementation of Istio for service mesh capabilities.

This repository serves as a comprehensive solution for managing and deploying infrastructure components efficiently. If you have any questions or need further assistance, feel free to reach out.


## Prerequisites

Before running Terraform, make sure you have the necessary credentials and permissions. Additionally, check and update variable values in the respective module directories as needed.

## Usage

To deploy a specific module, navigate to its directory and run the following commands:

```bash
cd path/to/module
terraform init
terraform apply
