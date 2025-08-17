#!/usr/bin/env bash
set -euo pipefail

# bootstrap_app_ec2.sh APP_PUBLIC_IP SSH_USER SSH_KEY_PATH
# Installs Docker, Docker Compose, Git, Python venv on App-EC2, deploys the dashboard
# via docker-compose, and installs Node Exporter as a systemd service.

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 APP_PUBLIC_IP SSH_USER SSH_KEY_PATH" >&2
  exit 1
fi

APP_PUBLIC_IP="$1"
SSH_USER="$2"
SSH_KEY_PATH="$3"

SSH_OPTS=(-o StrictHostKeyChecking=no -i "$SSH_KEY_PATH")

REMOTE_CMDS='set -euo pipefail
sudo apt update && sudo apt install -y docker.io docker-compose git python3-venv
if ! groups $USER | grep -q docker; then sudo usermod -aG docker $USER || true; fi

if [ ! -d ai-smartcloudops ]; then
  git clone https://github.com/Dileepreddy93/ai-smartcloudops.git
fi
cd ai-smartcloudops

python3 -m venv .venv || true
source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=src python - <<PY
from main import run_pipeline
run_pipeline("data/metrics.json")
print("metrics ready")
PY

docker compose up -d dashboard

# Install Node Exporter if not already
if ! command -v node_exporter >/dev/null 2>&1; then
  curl -fsSL https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-*.linux-amd64.tar.gz \
    | sudo tar -xz -C /usr/local/bin --strip-components=1 --wildcards "*/node_exporter"
fi
sudo bash -c "cat >/etc/systemd/system/node_exporter.service <<'EOF'
[Unit]
Description=Node Exporter
After=network.target

[Service]
ExecStart=/usr/local/bin/node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF"
sudo systemctl enable --now node_exporter
'

ssh "${SSH_OPTS[@]}" "$SSH_USER@$APP_PUBLIC_IP" "$REMOTE_CMDS"

echo "App-EC2 bootstrap done. Verify:"
echo "  http://$APP_PUBLIC_IP:5000/health"
echo "  http://$APP_PUBLIC_IP:9100/metrics"


