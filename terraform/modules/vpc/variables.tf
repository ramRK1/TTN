variable "create_vpc" {
  description = "Controls if VPC should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "cidr" {
  description = "The CIDR block for the VPC. Default value is a valid CIDR, but not acceptable by AWS and should be overridden"
#  type        = string
#  default     = "0.0.0.0/0"
  default      = "25.10.0.0/16"
}

variable "instance_tenancy" {
  description = "A tenancy option for instances launched into the VPC"
#  type        = string
  default     = "default"
}

variable "vpc_tags" {
  description = "Additional tags for the VPC"
  #type        = map(string)
  default     = "ram-vpc"
}
