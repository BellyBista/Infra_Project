module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "${var.project}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  enable_flow_log                     = true
  create_flow_log_cloudwatch_iam_role = true
  #create_flow_log_cloudwatch_log_group = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = 1
  }
}

resource "aws_kms_key" "mykey" {
  description             = "My example KMS key"
  deletion_window_in_days = 30   # Optional: Set the key deletion window (1 to 30 days)
  enable_key_rotation     = true # Optional: Enable key rotation

}

#  "Ensure KMS key Policy is defined"
data "aws_iam_policy_document" "kms_key_policy" {
  # Define your KMS key policy document here using the aws_iam_policy_document data source
  statement {
    actions   = ["kms:Decrypt", "kms:Encrypt", "kms:ReEncrypt*", "kms:GenerateDataKey*", "kms:Describe*"]
    resources = [aws_kms_key.mykey.arn]
    effect    = "Allow"
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.example.arn] #["arn:aws:iam::979187922977:user/Quadri"] # Replace with the AWS principal you want to grant access to
    }
  }
}

resource "aws_kms_key_policy" "mykey" {
  key_id = aws_kms_key.mykey.id
  policy = data.aws_iam_policy_document.kms_key_policy.json
}

resource "aws_flow_log" "example" {
  iam_role_arn    = aws_iam_role.example.arn
  log_destination = aws_cloudwatch_log_group.flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = module.vpc.vpc_id
}

resource "aws_cloudwatch_log_group" "flow_log" {
  name       = "vpc-flow-logs-to-cloudwatch-${random_pet.this.id}"
  kms_key_id = aws_kms_key.mykey.id
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["vpc-flow-logs.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "example" {
  name               = "example"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "example" {
  statement {
    effect = "Deny"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]

    resources = ["*"]
    condition {
      test     = "BoolIfExists"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_iam_role_policy" "example" {
  name   = "example"
  role   = aws_iam_role.example.id
  policy = data.aws_iam_policy_document.example.json
}

resource "random_pet" "this" {
  length = 2
}