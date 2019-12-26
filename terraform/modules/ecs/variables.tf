variable "cluster_tag" {
  description = "Additional tag for the cluster"
  default = "ram-cluster"
}

variable "tg_arn" {
  description = "It will give the ARN of the target group for the service"
  type = string
  default = ""
}

variable "subnets_id" {
  description = "It will give the list of subnet ids for the service"
  type = list(string)
  default = []
}

variable "sg_id" {
  description = "It will give the list of security group ids for the service"
  type = list(string)
  default = []
}

# variable "listener" {
#   description = "It will give the listener module for the service"
#   type = string
#   default = ""
# }

variable "load_balancer_arn" {
  description = "It will give the Load Balancer ARN for the listener"
  type = string
  default = ""
}