module "iam" {
  source = "./modules/iam/"
}

module "lt" {
  source = "./modules/lt/"
  volume_size = 20
  ami_id = "ami-04b9e92b5572fa0d1"
  instance_type = "t2.micro"
  key_name = "ramramkey"
  az_name = "us-east-1a"
  sg_id = var.sg_id
  iam_instance_profile = module.iam.iam_name
}

module "asg" {
  source = "./modules/asg/"
  lt_id = module.lt.lt_id
  vpc_zone_identifier = var.vpc_zone_identifier
  max_size = "3"
  min_size = "1"
  desired_capacity = "2"
  target_group_arns = var.tg_id
  default_cooldown = 250
}