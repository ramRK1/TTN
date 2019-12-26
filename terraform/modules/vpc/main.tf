######
# VPC
######
resource "aws_vpc" "ram" {
#  count = var.create_vpc ? 1 : 0

  cidr_block                       = var.cidr
  instance_tenancy                 = var.instance_tenancy

  tags = {
    Name = var.vpc_tags
  }
}

module "subnets" {
  source = "./modules/subnets/"
#  name = "ram-subnets"
  vpc_id = aws_vpc.ram.id
  public_subnet1 = "25.10.0.0/24"
}

module "igw" {
  source = "./modules/igw/"
  vpc_id = aws_vpc.ram.id
}

# module "nat" {
#   source = "./modules/nat/"
#   subnet_id = module.subnets.subnet_public_id1
# #  igw_path = module.igw.igw_path
# }

module "route" {
  source = "./modules/route/"
  vpc_id = aws_vpc.ram.id
  igw_id = module.igw.igw_id
  subnet_id1 = module.subnets.subnet_public_id1
  subnet_id2 = module.subnets.subnet_public_id2
}

module "sg" {
  source = "./modules/sg/"
  vpc_id = aws_vpc.ram.id
}