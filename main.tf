provider "aws" {
  region = "us-east-1" 
}

# Configura un grupo de seguridad para permitir SSH
resource "aws_security_group" "gpu_sg" {
  name_prefix = "gpu-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Limita a tu IP si es posible
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Crea la instancia EC2 y asocia el grupo de seguridad
resource "aws_instance" "gpu_instance" {
  ami               = "ami-0cda377a1b884a1bc"
  instance_type     = "g4dn.xlarge"
  key_name          = "my_key.pub" # Cambia al nombre de tu clave SSH
  security_groups   = [aws_security_group.gpu_sg.name]

  tags = {
    Name = "GPU-Instance"
  }
}
