#!/usr/bin/env bash
set -euo pipefail

# aws_prereq_setup.sh
# Idempotent AWS prerequisites setup for ai-smartcloudops Phase 7.
# - Detect admin IP
# - Find latest Ubuntu 22.04 AMI in REGION
# - Ensure key pair exists
# - Ensure default VPC/subnet
# - Ensure SGs exist with required ingress rules
# - Emit scripts/aws_env.sh with exports

: "${REGION:=us-east-1}"
: "${KEY_NAME:=ai-smartcloudops-key}"
: "${SG_APP_NAME:=ai-smartcloudops-app-sg}"
: "${SG_MON_NAME:=ai-smartcloudops-mon-sg}"

require_bin() { command -v "$1" >/dev/null 2>&1 || { echo "Missing binary: $1" >&2; exit 1; }; }
require_bin aws
require_bin curl

mkdir -p scripts

echo "[1/8] Detecting admin IP ..."
ADMIN_IP=$(curl -s ifconfig.me || true)
if [[ -z "${ADMIN_IP}" ]]; then
  echo "Could not detect admin IP via ifconfig.me" >&2
  exit 1
fi
echo "ADMIN_IP=${ADMIN_IP}"

echo "[2/8] Finding latest Ubuntu 22.04 AMI in ${REGION} ..."
AMI_ID=$(aws ec2 describe-images --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
  --query 'Images | sort_by(@,&CreationDate)[-1].ImageId' --output text --region "$REGION")
if [[ -z "${AMI_ID}" || "${AMI_ID}" == "None" ]]; then
  echo "Failed to resolve Ubuntu 22.04 AMI in region ${REGION}" >&2
  exit 1
fi
echo "AMI_ID=${AMI_ID}"

echo "[3/8] Ensuring EC2 key pair '${KEY_NAME}' exists ..."
set +e
aws ec2 describe-key-pairs --key-names "$KEY_NAME" --region "$REGION" >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
  set -e
  echo "Creating key pair ${KEY_NAME} ..."
  mkdir -p ~/.ssh
  aws ec2 create-key-pair --key-name "$KEY_NAME" --region "$REGION" \
    --query 'KeyMaterial' --output text > ~/.ssh/${KEY_NAME}.pem
  chmod 400 ~/.ssh/${KEY_NAME}.pem
else
  set -e
  echo "Key pair exists; reusing ${KEY_NAME}"
fi

echo "[4/8] Ensuring default VPC and a subnet ..."
VPC_ID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --region "$REGION" \
  --query 'Vpcs[0].VpcId' --output text)
if [[ -z "${VPC_ID}" || "${VPC_ID}" == "None" ]]; then
  echo "No default VPC found in ${REGION}. Please supply VPC/subnet manually." >&2
  exit 1
fi
SUBNET_ID=$(aws ec2 describe-subnets --filters Name=vpc-id,Values="$VPC_ID" --region "$REGION" \
  --query 'Subnets[0].SubnetId' --output text)
if [[ -z "${SUBNET_ID}" || "${SUBNET_ID}" == "None" ]]; then
  echo "No subnet found in VPC ${VPC_ID}." >&2
  exit 1
fi
echo "VPC_ID=${VPC_ID}"
echo "SUBNET_ID=${SUBNET_ID}"

echo "[5/8] Ensuring security groups exist ..."
# Helper to get SG id by group name within VPC
get_sg_id() {
  local name="$1"
  aws ec2 describe-security-groups --region "$REGION" \
    --filters Name=group-name,Values="$name" Name=vpc-id,Values="$VPC_ID" \
    --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null || true
}

SG_APP=$(get_sg_id "$SG_APP_NAME")
if [[ -z "$SG_APP" || "$SG_APP" == "None" ]]; then
  SG_APP=$(aws ec2 create-security-group --region "$REGION" \
    --group-name "$SG_APP_NAME" --description "ai-smartcloudops App SG" \
    --vpc-id "$VPC_ID" --query 'GroupId' --output text)
  echo "Created SG_APP ${SG_APP} (${SG_APP_NAME})"
else
  echo "SG_APP exists: ${SG_APP} (${SG_APP_NAME})"
fi

SG_MON=$(get_sg_id "$SG_MON_NAME")
if [[ -z "$SG_MON" || "$SG_MON" == "None" ]]; then
  SG_MON=$(aws ec2 create-security-group --region "$REGION" \
    --group-name "$SG_MON_NAME" --description "ai-smartcloudops Mon SG" \
    --vpc-id "$VPC_ID" --query 'GroupId' --output text)
  echo "Created SG_MON ${SG_MON} (${SG_MON_NAME})"
else
  echo "SG_MON exists: ${SG_MON} (${SG_MON_NAME})"
fi

echo "[6/8] Authorizing ingress rules (idempotent) ..."
# Function to add a CIDR rule if not present
allow_cidr() {
  local sg="$1" port="$2" cidr="$3"
  aws ec2 authorize-security-group-ingress --region "$REGION" \
    --group-id "$sg" --ip-permissions \
    IpProtocol=tcp,FromPort=$port,ToPort=$port,IpRanges='[{CidrIp="'"$cidr"'"}]' >/dev/null 2>&1 || true
}
# Function to add SG source rule if not present
allow_sg() {
  local sg="$1" port="$2" src_sg="$3"
  aws ec2 authorize-security-group-ingress --region "$REGION" \
    --group-id "$sg" --ip-permissions \
    IpProtocol=tcp,FromPort=$port,ToPort=$port,UserIdGroupPairs='[{GroupId="'"$src_sg"'"}]' >/dev/null 2>&1 || true
}

# App-EC2: 5000, 9100 from admin IP; 9100 from Mon-EC2 SG
allow_cidr "$SG_APP" 5000 "$ADMIN_IP/32"
allow_cidr "$SG_APP" 9100 "$ADMIN_IP/32"
allow_sg   "$SG_APP" 9100 "$SG_MON"

# Mon-EC2: 9090, 3000 from admin IP; 9100 from self and App-EC2 (optional)
allow_cidr "$SG_MON" 9090 "$ADMIN_IP/32"
allow_cidr "$SG_MON" 3000 "$ADMIN_IP/32"
allow_sg   "$SG_MON" 9100 "$SG_MON"
allow_sg   "$SG_MON" 9100 "$SG_APP"

echo "[7/8] Writing environment exports to scripts/aws_env.sh ..."
cat > scripts/aws_env.sh << ENV
export REGION=${REGION}
export AMI_ID=${AMI_ID}
export KEY_NAME=${KEY_NAME}
export SUBNET_ID=${SUBNET_ID}
export SG_APP=${SG_APP}
export SG_MON=${SG_MON}
export ADMIN_IP=${ADMIN_IP}
ENV
chmod +x scripts/aws_env.sh

echo "[8/8] Done. Suggested next steps:"
echo "  source scripts/aws_env.sh"
echo "  ./scripts/aws_setup.sh   # to launch EC2s and fetch IPs"
echo "  # then run bootstrap_app_ec2.sh and bootstrap_mon_ec2.sh as instructed"


