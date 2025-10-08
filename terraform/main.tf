provider "aws" {
  region = "us-east-1"
  profile = "test-devops"
  
}

resource "aws_instance" "from_launch_template" {
  launch_template {
    name    = "ecommerce"  # Replace with your template name
    version = "$Latest"                      # Or specific version like "1"
  }

  # Optionally tag the instance
  tags = {
    Name = "e-commerce"
  }
}

output "instance_public_ip" {
  value = aws_instance.from_launch_template.public_ip
  description = "The public IP of the EC2 instance"
}

