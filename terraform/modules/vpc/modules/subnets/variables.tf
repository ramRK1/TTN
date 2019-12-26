variable "create_vpc" {
  description = "Controls if VPC should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "vpc_id" {
    description = "It fetches vpc id for the use"
    type = string
    default = ""
}

variable "create_public_subnet1" {
  description = "Controls if public subnet 1 should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "public_subnet1" {
  description = "A public subnet 1 inside the VPC"
  type = string
  default     = ""
}

variable "public_az1" {
    description = "A availability zone 1 inside the VPC"
    default     = "us-east-1a"
}

variable "public_subnet_tag1" {
    description = "Additional tags for the public subnet 1"
    default     = "ram-public-subnet1"
}

variable "create_public_subnet2" {
  description = "Controls if public subnet 2 should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "public_subnet2" {
  description = "A public subnet 2 inside the VPC"
  default     = "25.10.1.0/24"
}

variable "public_az2" {
    description = "A availability zone 2 inside the VPC"
    default     = "us-east-1b"
}

variable "public_subnet_tag2" {
    description = "Additional tags for the public subnet 2"
    default     = "ram-public-subnet2"
}

variable "create_private_subnet1" {
  description = "Controls if private subnet 1 should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "private_subnet1" {
  description = "A private subnets inside the VPC"
  default     = "25.10.2.0/24"
}

variable "private_az1" {
    description = "A availability zone 1 inside the VPC"
    default     = "us-east-1a"
}

variable "private_subnet_tag1" {
    description = "Additional tags for the private subnet 1"
    default     = "ram-private-subnet1"
}

variable "create_private_subnet2" {
  description = "Controls if private subnet 2 should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "private_subnet2" {
  description = "A private subnets inside the VPC"
  default     = "25.10.3.0/24"
}

variable "private_az2" {
    description = "A availability zone 2 inside the VPC"
    default     = "us-east-1b"
}

variable "private_subnet_tag2" {
    description = "Additional tags for the private subnet 2"
    default     = "ram-private-subnet2"
}