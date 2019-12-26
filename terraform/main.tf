provider "aws" {
	region = "us-east-1"
}

module "vpc" {
	source = "./modules/vpc/"
}

# module "lb" {
# 	source = "./modules/lb/"
# 	vpc_id = module.vpc.vpc_id
# 	sg_id = [module.vpc.sg_id]
# 	subnets_id = [module.vpc.subnet_public_id1 ,module.vpc.subnet_public_id2]
# }

# module "asg" {
# 	source = "./modules/asg/"
# 	sg_id = [module.vpc.sg_id]
# 	tg_id = [module.lb.tg_id]
# 	vpc_zone_identifier = [module.vpc.subnet_public_id1 ,module.vpc.subnet_public_id2]
# }

#module "ecs" {
#        source = "./modules/ecs/"
#        tg_arn = module.lb.tg_arn
#        subnets_id = [module.vpc.subnet_public_id1 ,module.vpc.subnet_public_id2]
#        sg_id = [module.vpc.sg_id]
#        #listener = module.lb.listener
#        load_balancer_arn = module.lb.load_balancer_arn
#}
