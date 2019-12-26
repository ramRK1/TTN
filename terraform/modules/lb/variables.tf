variable "vpc_id" {
  description = "It will give the vpc id for the target group"
  type = string
  default = ""
}

variable "sg_id" {
  description = "It will give the list of security group ids"
  type = list(string)
  default = []
}

variable "subnets_id" {
  description = "It will give the list of subnet ids"
  type = list(string)
  default = []
}