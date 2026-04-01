#!/bin/bash
# aws/setup_ec2.sh
# User-data script to bootstrap the EC2 App Server for the Quiz API

# 1. Update and install dependencies
yum update -y
yum install -y python3 python3-pip git mariadb105-server curl

# 2. Setup application directory
mkdir -p /opt/cloudquiz
cd /opt/cloudquiz

# 3. Normally, we would clone the git repo here:
# git clone https://github.com/yourusername/online-quiz-system.git .
# For this script's purpose, we assume files are synced or cloned.

# 4. Install python dependencies
pip3 install flask flask-sqlalchemy flask-jwt-extended flask-cors pymysql boto3 python-dotenv gunicorn

# 5. Create Systemd Service for Gunicorn
cat <<EOF > /etc/systemd/system/cloudquiz.service
[Unit]
Description=Gunicorn instance to serve CloudQuiz API
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/cloudquiz/backend
Environment="PATH=/usr/local/bin"
# IMPORTANT: Provide RDS parameters in the actual environment or .env file
EnvironmentFile=/opt/cloudquiz/backend/.env
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable and start service
systemctl daemon-reload
systemctl start cloudquiz
systemctl enable cloudquiz

echo "Setup Complete. Gunicorn running on port 5000."
