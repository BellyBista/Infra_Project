resource "aws_iam_role" "test_oidc" {
  assume_role_policy = data.aws_iam_policy_document.test_oidc_assume_role_policy.json
  name               = "test-oidc"
}

resource "aws_iam_policy" "test-policy" {
  name = "test-policy"

  policy = jsonencode({
    Statement = [{
      Action = [
        "s3:*",
        "s3:ListAllMyBuckets", 
        "s3:GetBucketLocation"
      ]
      Effect   = "Allow"
      Resource = "*"
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "test_attach" {
  role       = aws_iam_role.test_oidc.name
  policy_arn = aws_iam_policy.test-policy.arn
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [ data.external.thumbprint.result.thumbprint ]
  url             = data.aws_eks_cluster.my-cluster.identity[0].oidc[0].issuer
}