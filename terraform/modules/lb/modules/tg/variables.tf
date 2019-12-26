variable "port_no" {
  description = "It will give the port number for the target group"
  type = number
  default = 80
}

variable "protocol" {
  description = "It will give the protocol for the target group"
  type = string
  default = "HTTP"
}

variable "vpc_id" {
  description = "It will give the vpc id for the target group"
  type = string
  default = ""
}

variable "load_balancer_depends" {
  description = "It will pass the whole load balancer block dependency to target group"
  type = string
}