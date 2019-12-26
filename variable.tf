variable "vpc_id" {
  type = ""
}

variable "sg_name_tag" {
  default = "sgCacheCluster"
}

variable "cache_name" {
  type = ""
}

variable "instance_type" {
  default = "t2.micro"
}

variable "desired_clusters" {
  default = 1
}

variable "parameter_group" {
  type = ""
}

variable "cluster_name_tag" {
  default = "CacheCluster"
}