resource "aws_lb_target_group" "ram-tg" {
  name     = "ram-tg"
  port     = var.port_no
  protocol = var.protocol
  vpc_id   = var.vpc_id
  depends_on = [aws_lb.ram-lb]
}

resource "aws_lb" "ram-lb" {
  name               = "ram-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.sg_id
  subnets            = var.subnets_id

#   enable_deletion_protection = true

#   access_logs {
#     bucket  = "${aws_s3_bucket.lb_logs.bucket}"
#     prefix  = "test-lb"
#     enabled = true
#   }

  tags = {
    Name = "ram-lb"
  }
}

resource "aws_lb_listener" "ram-listener" {
  load_balancer_arn = aws_lb.ram-lb.arn
  port              = var.port_no
  protocol          = var.protocol

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.ram-tg.arn #var.tg_arn
    # type = "redirect"

#     # redirect {
#     #   port        = "443"
#     #   protocol    = "HTTPS"
#     #   status_code = "HTTP_301"
#     # }
  }
}