#!/usr/bin/env bash
set -euo pipefail

# bootstrap_mon_ec2.sh MON_PUBLIC_IP SSH_USER SSH_KEY_PATH APP_PUBLIC_IP
# Installs Docker, Docker Compose, Git, Python venv on Mon-EC2, deploys Prometheus & Grafana,
# updates config/aws_targets.json with provided IPs, and regenerates file_sd.

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 MON_PUBLIC_IP SSH_USER SSH_KEY_PATH APP_PUBLIC_IP" >&2
  exit 1
fi

MON_PUBLIC_IP="$1"
SSH_USER="$2"
SSH_KEY_PATH="$3"
APP_PUBLIC_IP="$4"

SSH_OPTS=(-o StrictHostKeyChecking=no -i "$SSH_KEY_PATH")

REMOTE_CMDS='set -euo pipefail
sudo apt update && sudo apt install -y docker.io docker-compose git python3-venv jq
if ! groups $USER | grep -q docker; then sudo usermod -aG docker $USER || true; fi

if [ ! -d ai-smartcloudops ]; then
  git clone https://github.com/Dileepreddy93/ai-smartcloudops.git
fi
cd ai-smartcloudops

python3 -m venv .venv || true
source .venv/bin/activate
pip install -r requirements.txt

jq --arg appip "$APP_PUBLIC_IP" --arg monip "$MON_PUBLIC_IP" \
  \'{app:[($appip+":5000")],node_exporter:[($appip+":9100"),($monip+":9100")] }\' \
  <<<\'{}\' > config/aws_targets.json

python -m infra.scripts.prometheus_config --config config/aws_targets.json --out infra/prometheus/file_sd/app-and-node.json

docker compose up -d prometheus grafana
'

ssh "${SSH_OPTS[@]}" "$SSH_USER@$MON_PUBLIC_IP" "$REMOTE_CMDS"

echo "Mon-EC2 bootstrap done. Verify:"
echo "  http://$MON_PUBLIC_IP:9090/-/ready"
echo "  http://$MON_PUBLIC_IP:3000/api/health"


