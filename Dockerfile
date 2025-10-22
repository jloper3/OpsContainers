FROM ubuntu:24.04

LABEL maintainer="John Loper"
LABEL description="Reusable CLI environments for DevOps workflows"

ARG UID=1000
ARG GID=1000
ARG USERNAME=dev

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color

# Base packages
RUN apt-get update && \
    apt-get install -y \
      sudo curl git zsh unzip wget build-essential \
      ca-certificates jq fzf \
      python3 python3-venv python3-pip \
      openssh-client gnupg lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g $GID $USERNAME && \
    useradd -m -s /usr/bin/zsh -u $UID -g $GID $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USERNAME
WORKDIR /home/$USERNAME

# oh-my-zsh + plugins 
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && \
    sed -i 's/plugins=(git)/plugins=(git fzf zsh-autosuggestions zsh-syntax-highlighting kubectl)/' ~/.zshrc && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# tfenv
RUN git clone https://github.com/tfutils/tfenv.git ~/.tfenv && \
    echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.zshrc && \
    sudo ln -s ~/.tfenv/bin/* /usr/local/bin

# nvm + Node.js LTS
ENV NVM_DIR="$HOME/.nvm"
RUN mkdir -p "$NVM_DIR" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install --lts && \
    nvm alias default 'lts/*' && \
    echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.zshrc

# uv + uvx
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Helm
USER root
RUN curl -fsSL https://get.helm.sh/helm-v3.13.5-linux-amd64.tar.gz -o /tmp/helm.tar.gz && \
    tar -zxvf /tmp/helm.tar.gz -C /tmp && \
    mv /tmp/linux-amd64/helm /usr/local/bin/helm && \
    chmod +x /usr/local/bin/helm && \
    rm -rf /tmp/helm*
USER $USERNAME

# Copy opscontainers package into container
COPY opscontainers /home/$USERNAME/opscontainers

WORKDIR /workspace
ENV PATH="$HOME/.local/bin:$PATH"

ENTRYPOINT ["/usr/bin/zsh"]
