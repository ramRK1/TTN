resource "aws_launch_template" "ram-lt" {
  name = "ram-lt"

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size = var.volume_size
    }
  }

#   capacity_reservation_specification {
#     capacity_reservation_preference = "open"
#   }

#   credit_specification {
#     cpu_credits = "standard"
#   }

#   disable_api_termination = true

#   ebs_optimized = true

#   elastic_gpu_specifications {
#     type = "test"
#   }

#   elastic_inference_accelerator {
#     type = "eia1.medium"
#   }

  iam_instance_profile {
    name = var.iam_instance_profile
  }

  image_id = var.ami_id

#  instance_initiated_shutdown_behavior = "terminate"

  # instance_market_options {
  #   market_type = "spot"
  # }

  instance_type = var.instance_type

#  kernel_id = "test"

  key_name = var.key_name

#   license_specification {
#     license_configuration_arn = "arn:aws:license-manager:eu-west-1:123456789012:license-configuration:lic-0123456789abcdef0123456789abcdef"
#   }

#   monitoring {
#     enabled = true
#   }

  # network_interfaces {
  #   associate_public_ip_address = true
  # }

  placement {
    availability_zone = var.az_name
  }

#  ram_disk_id = "test"

  vpc_security_group_ids = var.sg_id

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = var.tag_lt
    }
  }

  user_data = base64encode(file("${path.module}/script.sh"))
}