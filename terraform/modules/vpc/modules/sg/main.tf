##########################
# Security group with name
##########################
resource "aws_security_group" "ram_sg" {
#  count = var.create && false == var.use_name_prefix ? 1 : 0

  name        = var.sg_name
  description = var.sg_description
  vpc_id      = var.vpc_id

  tags = {
      Name = var.sg_tag
    }

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}