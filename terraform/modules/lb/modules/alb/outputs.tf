# output "listener" {
#   value = aws_lb_listener.ram-listener
# }

output "load_balancer_arn" {
  value = aws_lb.ram-lb.arn
}

output "tg_id" {
  value = aws_lb_target_group.ram-tg.id
}

output "tg_arn" {
  value = aws_lb_target_group.ram-tg.arn
}