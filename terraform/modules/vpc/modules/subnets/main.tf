################
# Public subnet
################
resource "aws_subnet" "public1" {
#  count = var.create_vpc && var.create_public_subnet1 ? 1 : 0

  vpc_id                          = var.vpc_id
  cidr_block                      = var.public_subnet1 #element(concat(var.public_subnets, [""]), count.index)
  availability_zone               = var.public_az1 #element(var.azs, count.index)
  map_public_ip_on_launch         = true

  tags = {
    Name = var.public_subnet_tag1
  }
}

resource "aws_subnet" "public2" {
#  count = var.create_vpc && var.create_public_subnet2 ? 1 : 0

  vpc_id                          = var.vpc_id
  cidr_block                      = var.public_subnet2 #element(concat(var.public_subnets, [""]), count.index)
  availability_zone               = var.public_az2 #element(var.azs, count.index)
  map_public_ip_on_launch         = true

  tags = {
    Name = var.public_subnet_tag2
  }
}

#################
# Private subnet
#################
resource "aws_subnet" "private1" {
#  count = var.create_vpc && var.create_private_subnet1 ? 1 : 0

  vpc_id                          = var.vpc_id
  cidr_block                      = var.private_subnet1 #var.private_subnets[count.index]
  availability_zone               = var.private_az1 #element(var.azs, count.index)

  tags = {
      Name = var.private_subnet_tag1
  }
}

resource "aws_subnet" "private2" {
#  count = var.create_vpc && var.create_private_subnet2 ? 1 : 0

  vpc_id                          = var.vpc_id
  cidr_block                      = var.private_subnet2 #var.private_subnets[count.index]
  availability_zone               = var.private_az2 #element(var.azs, count.index)

  tags = {
      Name = var.private_subnet_tag2
  }
}