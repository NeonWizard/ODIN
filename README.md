```
    ███████    ██████████   █████ ██████   █████
  ███░░░░░███ ░░███░░░░███ ░░███ ░░██████ ░░███
 ███     ░░███ ░███   ░░███ ░███  ░███░███ ░███
░███      ░███ ░███    ░███ ░███  ░███░░███░███
░███      ░███ ░███    ░███ ░███  ░███ ░░██████
░░███     ███  ░███    ███  ░███  ░███  ░░█████
 ░░░███████░   ██████████   █████ █████  ░░█████
   ░░░░░░░    ░░░░░░░░░░   ░░░░░ ░░░░░    ░░░░░
```

# ODIN
![Python Version](https://img.shields.io/badge/python-v3.7-blue)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/NeonWizard/ODIN/Unit%20Testing)
![GitHub Repo stars](https://img.shields.io/github/stars/neonwizard/odin?style=social)

A centralized API for my various GPT-2 neural networks.

ODIN is primarily a Flask RPC API. Token-based authentication is available to ensure only certain users can perform text generation. Adding neural networks to the API is as simple as dragging and dropping into the models folder. There is also a command-line tool to be able to quickly and locally test or use the core ODIN logic without having to go through the web API.

## Installation
```bash
# Download the project
sudo git clone https://github.com/NeonWizard/ODIN /opt/neuraltextserver
cd /opt/neuraltextserver

# Set up the python environment and packages
make update

# Install the systemd service config
make setup-systemd

# Verify the service status
sudo systemctl status neuraltextserver.service

# Install the NGINX config
sudo cp deployment/odin.deadtired.me /etc/nginx/sites-available/odin.deadtired.me
sudo ln -sf /etc/nginx/sites-available/odin.deadtired.me /etc/nginx/sites-enabled/odin.deadtired.me

# Set up HTTPS via Certbot
sudo certbot --nginx -d odin.deadtired.me
sudo service nginx restart
```
