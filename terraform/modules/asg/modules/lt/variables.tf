variable "volume_size" {
  description = "It defines the size of the ebs"
  type = number
  default = 8
}

variable "iam_instance_profile" {
  description = "It will give the IAM Instance Profile name"
  type = string
  default = ""
}


variable "ami_id" {
  description = "It will give the ami id for the instance image"
  type = string
  default = ""
}

variable "instance_type" {
  description = "It will give the type of which instance will be"
  type = string
  default = ""
}

variable "key_name" {
  description = "It is for the name of the key-pair that will be used"
  type = string
  default = ""
}

variable "az_name" {
  description = "It will give the name of the in which the launch template is defined"
  type = string
  default = ""
}

variable "sg_id" {
  description = "It will give the list of security groups name that will associate with the launch template"
  type = list(string)
  default = []
}

variable "tag_lt" {
  description = "Additional tag for the launch template"
  default = "ram-lt"
}