###################
# Internet Gateway
###################
resource "aws_internet_gateway" "igw" {
#  count = var.create_vpc ? 1 : 0

  vpc_id = var.vpc_id

  tags = {
    Name = var.igw_tag
  }
}

# resource "aws_egress_only_internet_gateway" "outbound" {
# #  count = var.create_vpc ? 1 : 0

#   vpc_id = var.vpc_id
# }