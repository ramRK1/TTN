resource "aws_lb_listener" "ram-listener" {
  load_balancer_arn = var.load_balancer_arn
  port              = "80" #var.port_no
  protocol          = "HTTP" #var.protocol

  default_action {
    type = "forward"
    target_group_arn = var.tg_arn
  }
}

resource "aws_ecs_service" "ram-nginx-service" {
  name = var.service_name
  cluster = var.cluster_arn
  task_definition = var.task_arn
  desired_count = var.desired_count
  scheduling_strategy = "REPLICA"
  deployment_maximum_percent = 150
  deployment_minimum_healthy_percent = 50
#  iam_role        = var.iam_arn
#  depends_on      = ["aws_iam_role_policy.foo"]

  ordered_placement_strategy {
    type  = "spread"
    field = "instanceId"
  }

  load_balancer {
    target_group_arn = var.tg_arn
    container_name   = var.container_name
    container_port   = var.container_port
  }

#   network_configuration {
#     subnets = var.subnets_id
#     security_groups = var.sg_id
#   }

#   placement_constraints {
#     type       = "memberOf"
#     expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
#   }
depends_on = [aws_lb_listener.ram-listener]
}