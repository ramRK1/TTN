resource "aws_lb_target_group" "ram-tg" {
  name     = "ram-tg"
  port     = var.port_no
  protocol = var.protocol
  vpc_id   = var.vpc_id
  depends_on = [var.load_balancer_depends]
}