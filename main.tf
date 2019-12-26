#
# Security group resources
#
resource "aws_security_group" "memcached" {
  vpc_id = "${var.vpc_id}"

  tags {
    Name        = "${var.sg_name_tag}"
  }
}

#
# ElastiCache resources
#
resource "aws_elasticache_cluster" "memcached" {
  cluster_id             = "${lower(var.cache_name)}"
  engine                 = "memcached"
  #engine_version         = "${var.engine_version}"
  node_type              = "${var.instance_type}"
  num_cache_nodes        = "${var.desired_clusters}"
  #az_mode                = "${var.desired_clusters == 1 ? "single-az" : "cross-az"}"
  parameter_group_name   = "${var.parameter_group}"
  #subnet_group_name      = "${var.subnet_group}"
  security_group_ids     = ["${aws_security_group.memcached.id}"]
  #maintenance_window     = "${var.maintenance_window}"
  #notification_topic_arn = "${var.notification_topic_arn}"
  #port                   = "11211"

  tags {
    Name        = "${var.cluster_name_tag}"
  }
}