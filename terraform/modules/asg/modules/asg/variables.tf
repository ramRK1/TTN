variable "lt_id" {
  description = "It gives the launch template id"
  type = string
  default = ""
}

variable "vpc_zone_identifier" {
  description = "It gives the list of subnet ids for the auto-scaling group"
  type = list(string)
  default = []
}

variable "max_size" {
  description = "It will give the maximum limit of instances while scaling"
  type = string
}

variable "min_size" {
  description = "It will give the minimum limit of instances while scaling"
  type = string
}

variable "desired_capacity" {
  description = "It will give the desired limit of instance while scaling"
  type = string
}

variable "target_group_arns" {
  description = "A list of aws_alb_target_group ARNs, for use with Application Load Balancing"
  type = list(string)
  default = []
}

variable "default_cooldown" {
  description = "The amount of time, in seconds, after a scaling activity completes before another scaling activity can start"
  type        = number
  default     = 300
}

variable "tag_asg" {
  description = "Additional tag for auto-scaling group"
  default = "ram-asg"
}