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

variable "port_no" {
  description = "It will give the port number for load balancer"
  type = string
  default = "80"
}

variable "protocol" {
  description = "It will give the protocol for the load balancer"
  type = string
  default = "HTTP"
}

variable "tg_arn" {
  description = "It will give the target group ARN for the load balancer"
  type = string
  default = ""
}

variable "vpc_id" {
  description = "It will give the VPC ID for the target group"
  type = string
  default = ""
}
