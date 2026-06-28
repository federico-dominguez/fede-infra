# 🔑 Acceso a GitHub

## Token unificado

Todos los agentes comparten el mismo token de GitHub para simplificar la gestión.

| Atributo | Valor |
|----------|-------|
| **Token** | `ghp_5k…LITa` |
| **Scope** | `repo` (acceso completo a repositorios) |
| **Creado** | 2026-06-28 |
| **Propietario** | federico-dominguez |

## Agentes con acceso

| Agente | Dónde está configurado |
|--------|----------------------|
| 🐱 **Ticia** | Env var `GITHUB_TOKEN` del service `openclaw-ticia` |
| 🐶 **Claw** | Env var del contenedor Docker `moltbot-clawdbot-1` |
| 🧘 **Lina** | Env var del contenedor Docker (hereda de Claw) |
| 💎 **Gemma** | Env var del contenedor Docker (hereda de Claw) |
| 👀 **Mia** | Env var del service `goose-mia` en monitor-1 |
| 🐶 **Cline** | Env var del service `goose` en monitor-2 |

## Cómo usarlo desde un agente

```bash
# Verificar acceso
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos | python3 -c "import json,sys; [print(r['name']) for r in json.load(sys.stdin)]"

# Clonar repo de documentación
git clone https://federico-dominguez:***}@github.com/federico-dominguez/fede-infra.git

# O más seguro: usando GIT_ASKPASS
echo "echo \$GITHUB_TOKEN" > /tmp/git-askpass.sh
chmod +x /tmp/git-askpass.sh
GIT_ASKPASS=/tmp/git-askpass.sh git clone \
  https://federico-dominguez@github.com/federico-dominguez/fede-infra.git
```

## Renovación

Cuando expire o haya que rotar el token:

1. Crear nuevo token en https://github.com/settings/tokens
2. Actualizar en cada agente (o recrear el Docker con el nuevo token)
3. Actualizar este documento
