variable "vpc_id" {
    description = "It is used for giving path"
    type = string
    default = ""
}

variable "public_route_table_tag" {
  description = "Additional tag for public route table"
  default = "ram-public-rt"
}

variable "igw_id" {
  description = "It is for the internet gateway id"
  type = string
  default = ""
}

variable "subnet_id1" {
  description = "It is for public subnets ids"
  type = string
  default = ""
}

variable "subnet_id2" {
  description = "It is for public subnets ids"
  type = string
  default = ""
}