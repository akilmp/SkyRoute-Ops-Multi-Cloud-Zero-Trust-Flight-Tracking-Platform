resource "aws_iam_role" "edge_lambda" {
  name = "${var.environment}-edge-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = ["lambda.amazonaws.com", "edgelambda.amazonaws.com"]
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "edge_lambda_basic" {
  role       = aws_iam_role.edge_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "edge_lambda_kinesis" {
  role       = aws_iam_role.edge_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisFullAccess"
}

resource "aws_lambda_function" "edge" {
  function_name    = "${var.environment}-edge-lambda"
  role             = aws_iam_role.edge_lambda.arn
  handler          = "handler.handle"
  runtime          = "python3.11"
  filename         = "${path.module}/../../../services/edge-lambda/handler.zip"
  source_code_hash = filebase64sha256("${path.module}/../../../services/edge-lambda/handler.zip")
  publish          = true

  environment {
    variables = {
      TARGET_CLOUD   = var.edge_lambda_provider
      KINESIS_STREAM = aws_kinesis_stream.events.name
      PUBSUB_TOPIC   = var.edge_lambda_pubsub_topic
    }
  }
}

