resource "aws_iam_role" "replication" {
  name               = "tf-iam-role-replication-12345"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "replication" {
  name   = "tf-iam-role-policy-replication-12345"
  policy = data.aws_iam_policy_document.replication.json
}

resource "aws_iam_role_policy_attachment" "replication" {
  role       = aws_iam_role.replication.name
  policy_arn = aws_iam_policy.replication.arn
}

#1. S3 bucket
resource "aws_s3_bucket" "backend" {
  count = var.create_vpc ? 1 : 0

  bucket = lower("bootcamp32-${var.env}-${random_integer.s3.result}-east")

  tags = {
    Name        = "My bucket"
    Environment = var.env
  }
}

resource "aws_s3_bucket_versioning" "backend" {
  bucket = aws_s3_bucket.backend[0].id
  versioning_configuration {
    status = var.versioning
  }
}

resource "aws_s3_bucket" "source" {
  count    = var.create_vpc ? 1 : 0
  provider = aws.west
  bucket   = lower("bootcamp32-${var.env}-${random_integer.s3.result}-west")
  tags = {
    Name        = "My bucket"
    Environment = var.env
  }
}

resource "aws_s3_bucket_acl" "source_bucket_acl" {
  provider = aws.west

  bucket = aws_s3_bucket.source[0].id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "source" {
  provider = aws.west

  bucket = aws_s3_bucket.source[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.west
  # Must have bucket versioning enabled first
  depends_on = [aws_s3_bucket_versioning.source]

  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.source[0].id

  rule {
    id = "foobar"

    filter {
      prefix = "foo"
    }

    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.backend[0].arn
      storage_class = "STANDARD"
    }
  }
}

# Ensure that an S3 bucket has a lifecycle configuration
resource "aws_s3_bucket_lifecycle_configuration" "backend" {
  rule {
    id     = "backend-rule"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  bucket = aws_s3_bucket.backend[0].id
}

resource "aws_s3_bucket_lifecycle_configuration" "source" {
  rule {
    id     = "backend-rule"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  bucket = aws_s3_bucket.source[0].id
}

# Ensure that S3 bucket has a Public Access block
resource "aws_s3_bucket_public_access_block" "backend" {
  bucket = aws_s3_bucket.backend[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "source" {
  bucket = aws_s3_bucket.source[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


resource "aws_s3_bucket_logging" "backend" {
  bucket = aws_s3_bucket.backend[0].id

  target_bucket = aws_s3_bucket.backend[0].id
  target_prefix = "log/"
}

resource "aws_s3_bucket_logging" "source" {
  bucket = aws_s3_bucket.source[0].id

  target_bucket = aws_s3_bucket.source[0].id
  target_prefix = "log/"
}

#4. Random integer
resource "random_integer" "s3" {
  max = 100
  min = 1

  keepers = {
    bucket_env = var.env
  }
}

#5. KMS for bucket encryption
resource "aws_kms_key" "mykey" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

#  "Ensure KMS key Policy is defined"
data "aws_iam_policy_document" "kms_key_policy" {
  # Define your KMS key policy document here using the aws_iam_policy_document data source
  statement {
    actions   = ["kms:Decrypt", "kms:Encrypt", "kms:ReEncrypt*"]
    resources = [aws_kms_key.mykey.arn]
    effect    = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::123456789012:root"] # Replace with the AWS principal you want to grant access to
    }
  }
}

resource "aws_kms_key_policy" "mykey" {
  key_id = aws_kms_key.mykey.id
  policy = data.aws_iam_policy_document.kms_key_policy.json
}

#6. Bucket encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "backend" {
  bucket = aws_s3_bucket.backend[0].id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.mykey.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "source" {
  bucket = aws_s3_bucket.source[0].id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.mykey.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# Ensure S3 buckets should have event notifications enabled
resource "aws_s3_bucket_notification" "backend" {
  bucket = aws_s3_bucket.backend[0].id

  lambda_function {
    lambda_function_arn = "arn:aws:lambda:us-east-1:123456789012:function/YourLambdaFunction"
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "prefix/"
    filter_suffix       = ".txt"
  }

}

resource "aws_s3_bucket_notification" "source" {
  bucket = aws_s3_bucket.source[0].id

  lambda_function {
    lambda_function_arn = "arn:aws:lambda:us-east-1:123456789012:function/YourLambdaFunction"
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "prefix/"
    filter_suffix       = ".txt"
  }

}