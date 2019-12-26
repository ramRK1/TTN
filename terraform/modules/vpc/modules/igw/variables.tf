variable "create_vpc" {
  description = "Controls if VPC should be created (it affects almost all resources)"
  type        = bool
  default     = true
}

variable "igw_tag" {
    description = "Additional tags for the internet gateway"
    default     = "ram-igw"
}

variable "vpc_id" {
    description = "It is used for giving path"
    type = string
    default = ""
}