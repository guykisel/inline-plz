provider "microsoft-aws" {
  region = "us-east-27"
}

resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "ms2000.2xlarge"
}

