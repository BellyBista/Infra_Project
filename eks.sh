#!/bin/bash


# Set Terraform working directory
TERRAFORM_DIR="./"

# Function to run Terraform commands
run_terraform() {
    echo "Executing Terraform in $1 directory..."
    cd "$1" || exit
    terraform init
    terraform apply -auto-approve
    cd - || exit
}

# Function to prompt user for module choice
prompt_user() {
    read -p "Enter 'eks' or 'eks-cni' to run the corresponding Terraform module: " module_choice
    if [ "$module_choice" != "eks" ] && [ "$module_choice" != "eks-cni" ]; then
        echo "Invalid choice. Please enter 'eks' or 'eks-cni'."
        prompt_user
    fi
    run_terraform "$TERRAFORM_DIR/$module_choice"
}

# Execute Terraform modules in sequence

# 1. Run vpc-eks module
run_terraform "$TERRAFORM_DIR/vpc-eks"

# 2. Run eks module
prompt_user

# 3. Run security_group module
run_terraform "$TERRAFORM_DIR/security_group"

# 4. Run test-oidc module
run_terraform "$TERRAFORM_DIR/test-oidc"

# 5. Run autoscaling module
run_terraform "$TERRAFORM_DIR/autoscaling"

# 6. Run argocd module
run_terraform "$TERRAFORM_DIR/argocd"

# 7. Run efs module
run_terraform "$TERRAFORM_DIR/efs"

# 8. Run istio module
run_terraform "$TERRAFORM_DIR/istio"

echo "Sequence of runs completed."