variable "sg_id" {
  description = "It will give list of security group ids from the security group module"
  type = list(string)
  default = []
}

variable "vpc_zone_identifier" {
  description = "It will give list of subnet ids for the auto-scaling group"
  type = list(string)
  default = []
}

variable "tg_id" {
  description = "It will give list of target group ids"
  type = list(string)
  default = []
}