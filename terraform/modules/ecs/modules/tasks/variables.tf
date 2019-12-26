variable "family" {
  description = "It will give the name of the family for the task"
  default = "ram-nginx-task"
}

variable "network_mode" {
  description = "It will give network mode for the task"
  type = string
  default = "bridge"
}

variable "cpu" {
  description = "It will give the hard limit of the cpu for the task"
  type = number
  default = 128
}

variable "memory" {
  description = "It will give the hard limit of the memory for the task"
  type = number
  default = 256
}

variable "task_tag" {
  description = "Additional tag for the task"
  default = "ram-nginx-task"
}