output "tg_id" {
  value = module.alb.tg_id
}

output "tg_arn" {
  value = module.alb.tg_arn
}

# output "listener" {
#   value = module.alb.listener
# }

output "load_balancer_arn" {
  value = module.alb.load_balancer_arn
}