output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.ram.id
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = aws_vpc.ram.arn
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.ram.cidr_block
}

output "sg_id" {
  value = module.sg.sg_id
}

output "subnet_public_id1" {
  value = module.subnets.subnet_public_id1
}

output "subnet_public_id2" {
  value = module.subnets.subnet_public_id2
}