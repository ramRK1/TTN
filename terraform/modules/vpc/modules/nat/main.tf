resource "aws_nat_gateway" "nat" {
#  count = var.create_vpc && var.enable_nat_gateway ? local.nat_gateway_count : 0

  allocation_id = var.nat_gateway_ip
   
  subnet_id = var.subnet_id

  tags = {
    Name = var.nat_gateway_tag
  }

  #depends_on = [var.igw]
}