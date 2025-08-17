#!/usr/bin/env bash
set -euo pipefail

# aws_setup.sh
# Launch two Ubuntu EC2 instances (App-EC2 and Mon-EC2), wait for status OK,
# fetch public IPs, update config/aws_targets.json, regenerate Prometheus file_sd,
# and print export commands for live tests.

# Required env vars (or pass as arguments):
#   REGION          (e.g., us-east-1)
#   AMI_ID          (Ubuntu 22.04 AMI in your region)
#   KEY_NAME        (existing EC2 key pair name)
#   SUBNET_ID       (subnet-xxxxxxxx)
#   SG_APP          (security group id for App-EC2)
#   SG_MON          (security group id for Mon-EC2)
# Optional:
#   INSTANCE_TYPE   (default: t2.micro)

usage() {
  cat << USAGE
Usage: ENV vars must be set before running, e.g.:

  REGION=us-east-1 \
  AMI_ID=ami-xxxxxxxx \
  KEY_NAME=my-key \
  SUBNET_ID=subnet-xxxxxxxx \
  SG_APP=sg-aaaaaaaa \
  SG_MON=sg-bbbbbbbb \
  ./scripts/aws_setup.sh

USAGE
}

require() { if [ -z "${!1:-}" ]; then echo "Missing env var: $1"; usage; exit 1; fi; }

require REGION
require AMI_ID
require KEY_NAME
require SUBNET_ID
require SG_APP
require SG_MON

INSTANCE_TYPE=${INSTANCE_TYPE:-t2.micro}

echo "Launching EC2 instances in $REGION ..."

APP_ID=$(aws ec2 run-instances \
  --region "$REGION" \
  --image-id "$AMI_ID" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SG_APP" \
  --subnet-id "$SUBNET_ID" \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ai-app-ec2}]' \
  --query 'Instances[0].InstanceId' --output text)

MON_ID=$(aws ec2 run-instances \
  --region "$REGION" \
  --image-id "$AMI_ID" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SG_MON" \
  --subnet-id "$SUBNET_ID" \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ai-mon-ec2}]' \
  --query 'Instances[0].InstanceId' --output text)

echo "App-EC2: $APP_ID"
echo "Mon-EC2: $MON_ID"

echo "Waiting for both instances to be status-ok ..."
aws ec2 wait instance-status-ok --region "$REGION" --instance-ids "$APP_ID" "$MON_ID"

APP_PUBLIC_IP=$(aws ec2 describe-instances --region "$REGION" --instance-ids "$APP_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
MON_PUBLIC_IP=$(aws ec2 describe-instances --region "$REGION" --instance-ids "$MON_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "APP_PUBLIC_IP=$APP_PUBLIC_IP"
echo "MON_PUBLIC_IP=$MON_PUBLIC_IP"

# Update config/aws_targets.json locally using jq if present, else write a minimal file
CFG=config/aws_targets.json
mkdir -p config
if command -v jq >/dev/null 2>&1 && [ -f "$CFG" ]; then
  tmp=$(mktemp)
  jq --arg appip "$APP_PUBLIC_IP" --arg monip "$MON_PUBLIC_IP" \
     '.app=[($appip+":5000")] | .node_exporter=[($appip+":9100"),($monip+":9100")]' \
     "$CFG" > "$tmp"
  mv "$tmp" "$CFG"
else
  cat > "$CFG" << JSON
{
  "app": ["$APP_PUBLIC_IP:5000"],
  "node_exporter": ["$APP_PUBLIC_IP:9100", "$MON_PUBLIC_IP:9100"]
}
JSON
fi

# Regenerate Prometheus file_sd locally
python -m infra.scripts.prometheus_config --config "$CFG" \
  --out infra/prometheus/file_sd/app-and-node.json || true

# Persist env exports for convenience
cat > .env.live << ENV
export APP_PUBLIC_IP=$APP_PUBLIC_IP
export MON_PUBLIC_IP=$MON_PUBLIC_IP
export PROMETHEUS_URL=http://$MON_PUBLIC_IP:9090
export GRAFANA_URL=http://$MON_PUBLIC_IP:3000
ENV

echo
echo "Success. Export these in your shell:"
echo "  export APP_PUBLIC_IP=$APP_PUBLIC_IP"
echo "  export MON_PUBLIC_IP=$MON_PUBLIC_IP"
echo "  export PROMETHEUS_URL=http://$MON_PUBLIC_IP:9090"
echo "  export GRAFANA_URL=http://$MON_PUBLIC_IP:3000"
echo
echo "Next steps:"
echo "  1) SSH into App-EC2 ($APP_PUBLIC_IP) and run scripts/bootstrap_app_ec2.sh"
echo "  2) SSH into Mon-EC2 ($MON_PUBLIC_IP) and run scripts/bootstrap_mon_ec2.sh"
echo "  3) Then run: AWS_LIVE=1 PROMETHEUS_URL=... GRAFANA_URL=... pytest -q -m \"aws_live\""


