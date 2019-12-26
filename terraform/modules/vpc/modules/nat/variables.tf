variable "nat_gateway_ip" {
    description = "It is for the IP allocation for the nat gateway"
    default = "default"
}

variable "subnet_id" {
    description = "It is for the public subnet 1 IP"
    type = string
    default = ""
}

variable "igw_path" {
  description = "It will give the module access of internet gateway"
  type = string
  default = ""
}


variable "nat_gateway_tag" {
    description = "Additional tag is given to the nat gateway"
    default = "ram-nat"
}