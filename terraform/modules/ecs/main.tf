resource "aws_ecs_cluster" "ram-cluster" {
  name = "ram-cluster"
  tags = {
    name = var.cluster_tag
  }
}

module "tasks" {
  source = "./modules/tasks/"
}

module "service" {
  source = "./modules/service/"
  cluster_arn = aws_ecs_cluster.ram-cluster.arn
  task_arn = module.tasks.task_arn
  tg_arn = var.tg_arn
  subnets_id = var.subnets_id
  sg_id = var.sg_id
  load_balancer_arn = var.load_balancer_arn
#  listener = var.listener
}
