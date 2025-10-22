export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git terraform aws kubectl fzf zsh-autosuggestions zsh-syntax-highlighting kubectl)
source $ZSH/oh-my-zsh.sh

# Aliases
alias ll='ls -alF'
alias tf='terraform'
alias k='kubectl'
alias kctx='kubectl config use-context'
alias kns='kubectl config set-context --current --namespace'
alias h='helm'
alias hls='helm list'
alias hdep='helm dependency update'

alias awslogin='aws sso login'
alias mcp='python3 -m mcp_server.cli'
alias uvp='uv pip install'
alias uvr='uv run'

# Paths
export PATH="$HOME/.tfenv/bin:$PATH"
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export PATH="$HOME/.local/bin:$PATH"

export PS1="🌩️ [%n@%m] %~ $ "
