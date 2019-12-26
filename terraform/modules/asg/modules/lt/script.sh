#!/bin/bash -xe
# exec >> (tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
# cat <<'EOF' >> /etc/ecs/ecs.config
# ECS_CLUSTER=ram-cluster
# EOF
sudo apt-get update
sudo apt-get install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx