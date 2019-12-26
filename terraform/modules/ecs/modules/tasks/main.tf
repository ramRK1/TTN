resource "aws_ecs_task_definition" "ram-nginx-task" {
  family = var.family
  network_mode = var.network_mode
  cpu = var.cpu
  memory = var.memory
  requires_compatibilities = ["EC2"]
  container_definitions = file("${path.module}/nginx-container.json")

  tags = {
    Name = var.task_tag
  }

  # volume {
  #   name      = "nginx-storage"
  #   host_path = "/ecs/nginx-storage"
  # }

  # placement_constraints {
  #   type       = "memberOf"
  #   expression = "attribute:ecs.availability-zone in [us-east-1a, us-east-1b]"
  # }
}
