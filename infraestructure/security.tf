resource "aws_security_group" "flask_sg" {
  name        = "flask-sg"
  description = "Permitir trafego HTTP para Flask"
  vpc_id      = "vpc-0a08d9ee58c460e38" # Substitua pelo ID da sua VPC

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
