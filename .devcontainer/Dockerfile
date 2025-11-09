FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# ---- base toolchain
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    iptables iptables-persistent libcap2-bin curl ca-certificates git \
    python3 python3-pip python3-venv \
 && rm -rf /var/lib/apt/lists/*

# allow non-root iptables when NET_ADMIN present
RUN setcap cap_net_admin+ep /usr/sbin/iptables || true \
 && setcap cap_net_admin+ep /usr/sbin/ip6tables || true

# ---- Python venv + SDKs
ENV AI_VENV=/opt/ai/venv
RUN python3 -m venv $AI_VENV \
 && $AI_VENV/bin/pip install --upgrade pip \
 && $AI_VENV/bin/pip install --no-cache-dir google-generativeai anthropic openai huggingface_hub
ENV PATH="$AI_VENV/bin:${PATH}"

# ---- Node.js 20 (for CLIs)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

# Writable global npm prefix + PATH
RUN mkdir -p /opt/npm-global/bin && chown -R vscode:vscode /opt/npm-global
ENV NPM_CONFIG_PREFIX=/opt/npm-global
ENV PATH=/opt/npm-global/bin:$PATH

# ---- Install CLIs as non-root so no EACCES
USER vscode

# 1) ChatGPT Codex CLI (latest)
RUN npm install -g @openai/codex@latest

# 2) Google Gemini CLI (latest)
RUN npm install -g @google/gemini-cli@latest

# 3) (optional) Claude Code CLI — uncomment when needed
# RUN npm install -g @anthropic-ai/claude-code@latest

USER root

# ---- helpers
COPY ai_bootstrap.sh /usr/local/bin/ai_bootstrap.sh
COPY webonly-firewall.sh /usr/local/bin/webonly-firewall.sh
RUN chmod +x /usr/local/bin/ai_bootstrap.sh /usr/local/bin/webonly-firewall.sh \
 && sed -i 's/\r$//' /usr/local/bin/ai_bootstrap.sh /usr/local/bin/webonly-firewall.sh
