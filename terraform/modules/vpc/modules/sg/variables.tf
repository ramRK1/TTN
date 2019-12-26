variable "sg_name" {
  description = "It is for the security group name"
  default = "ram_sg"
}

variable "sg_description" {
  description = "It has the description about the security group"
  default = "security group for restrict the access for different protocols"
}

variable "vpc_id" {
  description = "It contains the vpc id"
  type = string
  default = ""
}

variable "sg_tag" {
  description = "Additional tag for the security group"
  default = ""
}
