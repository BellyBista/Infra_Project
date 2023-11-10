# Use the Jenkins base image
FROM jenkins/jenkins:lts

# Switch to root user for installations
USER root

# Install required packages
RUN apt-get update && \
    apt-get install -y curl nano ansible jq openssl java-common zip unzip git wget python3-pip rsync awscli ca-certificates sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Docker
RUN curl -fsSL https://get.docker.com | sh

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install Helm
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && \
    chmod +x get_helm.sh && \
    ./get_helm.sh

# Install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.5.3/terraform_1.5.3_linux_amd64.zip && \
    unzip terraform_1.5.3_linux_amd64.zip -d /usr/local/bin && \
    rm terraform_1.5.3_linux_amd64.zip

# Install pipx
RUN apt install -y python3.11-venv
ENV PATH="/opt/venv/bin:$PATH"
RUN apt install -y pipx

# Install boto3 using pipx
RUN pipx install boto3 --include-deps

# Switch back to the Jenkins user
USER jenkins

