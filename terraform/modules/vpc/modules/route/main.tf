################
# Publiс routes
################
resource "aws_route_table" "public" {
#  count = var.create_vpc && length(var.public_subnets) > 0 ? 1 : 0

  vpc_id = var.vpc_id

  tags = {
    Name = var.public_route_table_tag
  }
}

resource "aws_route" "public_internet_gateway" {
#  count = var.create_vpc && length(var.public_subnets) > 0 ? 1 : 0

  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = var.igw_id

#   timeouts {
#     create = "5m"
#   }
}

##########################
# Route table association
##########################
resource "aws_route_table_association" "public1" {
#  count = var.create_vpc && length(var.public_subnets) > 0 ? length(var.public_subnets) : 0

  subnet_id      = var.subnet_id1
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public2" {
#  count = var.create_vpc && length(var.public_subnets) > 0 ? length(var.public_subnets) : 0

  subnet_id      = var.subnet_id2
  route_table_id = aws_route_table.public.id
}

# #################
# # Private routes
# # There are as many routing tables as the number of NAT gateways
# #################
# resource "aws_route_table" "private" {
#   count = var.create_vpc && local.max_subnet_length > 0 ? local.nat_gateway_count : 0

#   vpc_id = local.vpc_id

#   tags = merge(
#     {
#       "Name" = var.single_nat_gateway ? "${var.name}-${var.private_subnet_suffix}" : format(
#         "%s-${var.private_subnet_suffix}-%s",
#         var.name,
#         element(var.azs, count.index),
#       )
#     },
#     var.tags,
#     var.private_route_table_tags,
#   )

#   lifecycle {
#     # When attaching VPN gateways it is common to define aws_vpn_gateway_route_propagation
#     # resources that manipulate the attributes of the routing table (typically for the private subnets)
#     ignore_changes = [propagating_vgws]
#   }
# }

# ##########################
# # Route table association
# ##########################
# resource "aws_route_table_association" "private" {
#   count = var.create_vpc && length(var.private_subnets) > 0 ? length(var.private_subnets) : 0

#   subnet_id = element(aws_subnet.private.*.id, count.index)
#   route_table_id = element(
#     aws_route_table.private.*.id,
#     var.single_nat_gateway ? 0 : count.index,
#   )
# }