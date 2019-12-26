# module "tg" {
#   source = "./modules/tg/"
#   port_no = 80
#   protocol = "HTTP"
#   vpc_id = var.vpc_id
# }

module "alb" {
  source = "./modules/alb/"
  sg_id = var.sg_id
  vpc_id = var.vpc_id
  subnets_id = var.subnets_id
  port_no = "80"
  protocol = "HTTP"
  #tg_arn = module.tg.tg_arn
}