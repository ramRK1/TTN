variable "service_name" {
  description = "It will give the name for the service"
  default = "ram-nginx-service"
}

variable "cluster_arn" {
  description = "It will give the ARN of the cluster for the service"
  type = string
  default = ""
}

variable "task_arn" {
  description = "It will give ARN of the task for the service"
  type = string
  default = ""
}

variable "desired_count" {
  description = "It will the desired count for the service"
  type = number
  default = 1
}

variable "iam_arn" {
  description = "It will give the IAM ARN for the service"
  type = string
  default = "arn:aws:iam::218619999254:role/ecsInstanceRole"
}


variable "tg_arn" {
  description = "It will give the ARN of the target group for the service"
  type = string
  default = ""
}

variable "container_name" {
  description = "It will give the container name for the service"
  type = string
  default = "ram-nginx-container"
}

variable "container_port" {
  description = "It will give the container port for the service"
  type = number
  default = 80
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
#   description = "It will give the listener resource block for the service"
#   type = string
#   default = ""
# }

variable "load_balancer_arn" {
  description = "It will give the Load Balancer ARN for the listener"
  type = string
  default = ""
}