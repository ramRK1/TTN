resource "aws_autoscaling_group" "ram-asg" {
#   count = var.create_asg && false == var.create_asg_with_initial_lifecycle_hook ? 1 : 0

#   name_prefix = "${join(
#     "-",
#     compact(
#       [
#         coalesce(var.asg_name, var.name),
#         var.recreate_asg_when_lc_changes ? element(concat(random_pet.asg_name.*.id, [""]), 0) : "",
#       ],
#     ),
#   )}-"
  launch_template {
    id = var.lt_id
    version = "$Latest"
  }
  vpc_zone_identifier  = var.vpc_zone_identifier
  max_size             = var.max_size
  min_size             = var.min_size
  desired_capacity     = var.desired_capacity

#   load_balancers            = var.load_balancers
#   health_check_grace_period = var.health_check_grace_period
#   health_check_type         = var.health_check_type

#   min_elb_capacity          = var.min_elb_capacity
#   wait_for_elb_capacity     = var.wait_for_elb_capacity
  target_group_arns         = var.target_group_arns
  default_cooldown          = var.default_cooldown
  # force_delete              = var.force_delete
  # termination_policies      = var.termination_policies
  # suspended_processes       = var.suspended_processes
  # placement_group           = var.placement_group
  # enabled_metrics           = var.enabled_metrics
  # metrics_granularity       = var.metrics_granularity
  # wait_for_capacity_timeout = var.wait_for_capacity_timeout
  # protect_from_scale_in     = var.protect_from_scale_in

  # tags = {
  #   Name = var.tag_asg
  #   key = "Name"
  #   value = "ram-terraform"
  #   propogate_on_launch = true
  # }
}

resource "aws_autoscaling_attachment" "asg_attachment_bar" {
  autoscaling_group_name = aws_autoscaling_group.ram-asg.id
  alb_target_group_arn   = var.target_group_arns[0]
}
