resource "aws_iam_role" "ram-ecs-instance-role" {
  name = "ram-ecs-instance-role"
  assume_role_policy = data.aws_iam_policy_document.ram-ecs-instance-policy.json
#  assume_role_policy = file("${path.module}/role.json")
}

data "aws_iam_policy_document" "ram-ecs-instance-policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_instance_profile" "ram-ecs-instance-profile" {
  name = "ram-ecs-instance-profile"
  role = aws_iam_role.ram-ecs-instance-role.name
}

resource "aws_iam_role_policy_attachment" "ram-ecs-instance-role-attachment" {
  role = aws_iam_role.ram-ecs-instance-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# resource "aws_iam_role_policy_attachment" "ecs_ec2_cloudwatch_role" {
#   role = aws_iam_role.ram-role.id
#   policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
# }