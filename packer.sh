#!/bin/bash

set -x

# Define variables
region="us-east-1"
team="g09"
env="dev"
ami_name="bootcamp32-${team}-${env}"
terraform_directory="/Users/quadribello/Infra_Project"
packer_folder="/Users/quadribello/Infra_Project/ami_packer"
packer_template="/Users/quadribello/Infra_Project/ami_packer/aws_docker.pkr.hcl"

# Check if the AMI exists in the specified region
if aws ec2 describe-images --region $region --filters "Name=name,Values=$ami_name" | grep -q "ImageId"; then
    echo "AMI $ami_name exists in $region."
else
    echo "AMI $ami_name does not exist in $region. Creating..."
    # Call Packer to create the AMI
    packer init $packer_folder
    packer fmt $packer_folder
    packer build -var 'ami_name'=$ami_name $packer_template

    # Wait for the AMI to become available
    echo "Waiting for the AMI to become available..."
    aws ec2 wait image-available --region $region --filters "Name=name,Values=$ami_name"
    echo "AMI $ami_name is now available."
fi

# Create a t2.micro instance using Terraform
cd $terraform_directory
terraform init
terraform apply -auto-approve -var "ami_name=$ami_name" 
terraform destroy -auto-approve -var "ami_name=$ami_name"