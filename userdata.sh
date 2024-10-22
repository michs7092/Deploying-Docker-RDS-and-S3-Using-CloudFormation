#!/bin/bash
sudo apt update -y
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo docker run -d -p 80:5000 public.ecr.aws/l2u5d2v6/webapp