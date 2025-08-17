# Deploy with Docker on AWS EC2

## Overview
- App-EC2: runs the Flask dashboard container (port 5000) and Node Exporter (9100)
- Mon-EC2: runs Prometheus (9090) and Grafana (3000)

## Prereqs
- Two Ubuntu 22.04 EC2 instances (t2.micro ok). Security groups:
  - App-EC2: allow 80/443, 5000, 9100 from Mon-EC2/Admin IP
  - Mon-EC2: allow 9090, 3000 from Admin IP, 9100 from App-EC2 and self
- Docker / docker-compose installed

## App-EC2 steps
```bash
sudo apt update && sudo apt install -y docker.io docker-compose git python3-venv
sudo usermod -aG docker $USER
newgrp docker

git clone https://github.com/Dileepreddy93/ai-smartcloudops.git
cd ai-smartcloudops
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
PYTHONPATH=src python -c 'from main import run_pipeline; run_pipeline("data/metrics.json")'

docker compose up -d dashboard
```
- Verify: http://APP_PUBLIC_IP:5000/health

## Node Exporter on App-EC2
```bash
curl -fsSL https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-*.linux-amd64.tar.gz | \
  sudo tar -xz -C /usr/local/bin --strip-components=1 --wildcards '*/node_exporter'
cat << 'EOF' | sudo tee /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target

[Service]
ExecStart=/usr/local/bin/node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now node_exporter
```
- Verify: http://APP_PUBLIC_IP:9100/metrics

## Mon-EC2 steps
```bash
sudo apt update && sudo apt install -y docker.io docker-compose git python3-venv
sudo usermod -aG docker $USER
newgrp docker

git clone https://github.com/Dileepreddy93/ai-smartcloudops.git
cd ai-smartcloudops
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python -m infra.scripts.prometheus_config --config config/aws_targets.json --out infra/prometheus/file_sd/app-and-node.json

# Edit config/aws_targets.json with your APP_PUBLIC_IP and MON_PUBLIC_IP
nano config/aws_targets.json

# Start Prometheus and Grafana
docker compose up -d prometheus grafana
```
- Verify Prometheus: http://MON_PUBLIC_IP:9090/-/ready
- Verify Grafana: http://MON_PUBLIC_IP:3000/ (admin/admin; password set via GF_SECURITY_ADMIN_PASSWORD)

## Update targets
- Edit `config/aws_targets.json` with your real IPs/ports:
```json
{
  "app": ["APP_PUBLIC_IP:5000"],
  "node_exporter": ["APP_PUBLIC_IP:9100", "MON_PUBLIC_IP:9100"]
}
```
- Regenerate file_sd:
```bash
python -m infra.scripts.prometheus_config --config config/aws_targets.json --out infra/prometheus/file_sd/app-and-node.json
```
- Redeploy/refresh Prometheus container if needed.

## Live checks (Phase 7)
```bash
export AWS_LIVE=1
export PROMETHEUS_URL=http://MON_PUBLIC_IP:9090
export GRAFANA_URL=http://MON_PUBLIC_IP:3000
pytest -q -m "aws_live"
```

## Hardening
- Put Nginx/ALB in front of dashboard
- Enable TLS (Let’s Encrypt or ACM)
- Lock down SGs to IP ranges or VPC
