# Configuração Manual do RClone

## Status Atual
❌ rclone não instalado no sistema

## Soluções

### Opção 1: Instalar via apt (requer sudo)
```bash
sudo apt update
sudo apt install rclone
rclone config
```

### Opção 2: Instalar manual (sem sudo)
```bash
# Baixar binário
cd ~
curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip
cd rclone-*-linux-amd64

# Copiar para local bin
mkdir -p ~/.local/bin
cp rclone ~/.local/bin/

# Adicionar ao PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verificar
rclone --version
```

### Opção 3: Usar scripts Python alternativos (já criados)
Usar `storage_lark.py` e `storage_baidu.py` que criamos (não precisam de rclone)

## Recomendação Para Seu Caso
Use **Opção 3** (scripts Python) enquanto não instala rclone.

Ou me informe quando puder rodar comando com sudo para instalar rclone oficial.
