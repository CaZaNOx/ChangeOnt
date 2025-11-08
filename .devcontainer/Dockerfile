FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# base toolchain
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    iptables iptables-persistent libcap2-bin curl ca-certificates git python3 python3-pip python3-venv \
 && rm -rf /var/lib/apt/lists/*

# allow non-root iptables when NET_ADMIN present
RUN setcap cap_net_admin+ep /usr/sbin/iptables || true \
 && setcap cap_net_admin+ep /usr/sbin/ip6tables || true

# Python venv + SDKs (no keys required to install)
ENV AI_VENV=/opt/ai/venv
RUN python3 -m venv $AI_VENV && $AI_VENV/bin/pip install --upgrade pip \
 && $AI_VENV/bin/pip install --no-cache-dir google-generativeai anthropic openai huggingface_hub
ENV PATH="$AI_VENV/bin:${PATH}"

# Node.js (CLIs)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

# Terminal AI CLIs
# 1) ChatGPT Codex CLI (uses ChatGPT Plus/Pro/etc login)
RUN npm install -g @openai/codex
# 2) Google Gemini CLI (free-tier)
RUN npm install -g @google/gemini-cli
# 3) (optional) Claude Code CLI — uncomment if you get Claude Pro/Max
# RUN curl -fsSL https://claude.ai/install.sh | bash

# helpers (kept inside .devcontainer/)
COPY ai_bootstrap.sh /usr/local/bin/ai_bootstrap.sh
COPY webonly-firewall.sh /usr/local/bin/webonly-firewall.sh
RUN chmod +x /usr/local/bin/ai_bootstrap.sh /usr/local/bin/webonly-firewall.sh \
 && sed -i 's/\r$//' /usr/local/bin/ai_bootstrap.sh /usr/local/bin/webonly-firewall.sh