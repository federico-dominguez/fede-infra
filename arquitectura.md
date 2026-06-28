# 🏗️ Arquitectura General

## Resumen

Red de **6 agentes de IA** funcionando 24/7 en **Oracle Cloud Free Tier**, comunicados por **Tailscale VPN**, con **OpenRouter** como proveedor unificado y claves de API independientes.

## Diagrama de red

```
┌─────────────────────────────────────────────────────────┐
│                    🌐 INTERNET                           │
└─────────────────────┬───────────────────────────────────┘
                      │ (solo puertos 80, 443)
          ┌───────────┴───────────┐
          │   🛡️ Security List    │
          │   (firewall OCI)      │
          └───────────┬───────────┘
                      │
          ┌───────────┴───────────┐
          │   🔗 Tailscale VPN    │
          │   (red privada mesh)  │
          └──┬───────┬───────┬───┘
             │       │       │
    ┌────────┴┐ ┌────┴────┐ ┌┴────────┐
    │  MAIN   │ │MONITOR-1│ │MONITOR-2│
    │  🐱     │ │  👀     │ │  🐶     │
    │A1.2/12GB│ │E2.1/1GB │ │E2.1/1GB │
    └────┬────┘ └─────────┘ └─────────┘
         │
    ┌────┴────┐
    │  Docker │
    │  🐳     │
    │Claw Lina│
    │ Gemma   │
    └─────────┘
```

## Especificaciones técnicas

### Oracle Cloud (sa-saopaulo-1)

| Recurso | Detalle |
|---------|---------|
| **Cuenta** | Free Tier (Always Free) |
| **Región** | São Paulo (sa-saopaulo-1) |
| **Instancias** | 3 (1 ARM + 2 AMD) |
| **VCN** | `10.0.0.0/16` |
| **Subnet** | `10.0.1.0/24` (pública) |

### Instancias

| Nombre | Shape | OCPU | RAM | Disco | SO |
|--------|-------|------|-----|-------|-----|
| **main** | VM.Standard.A1.Flex | 2 ARM | 12 GB | 47 GB | Ubuntu 22.04 |
| **monitor-1** | VM.Standard.E2.1.Micro | 1 AMD | 1 GB | 47 GB | Ubuntu 22.04 |
| **monitor-2** | VM.Standard.E2.1.Micro | 1 AMD | 1 GB | 47 GB | Ubuntu 22.04 |

## Proveedor de IA

**OpenRouter** — unificado para todos los agentes.

| Key | Propósito | Modelo |
|-----|-----------|--------|
| `main-key` | Ticia (OpenClaw nativo) | deepseek/deepseek-v4-pro |
| `main-moltbot-key` | Claw, Lina, Gemma (Docker) | deepseek/deepseek-v4-flash/pro |
| `monitor-1-key` | Mia (Goose) | deepseek/deepseek-v4-flash |
| `monitor-2-key` | Cline (Goose) | deepseek/deepseek-v4-flash |

## Respaldo

- Backups automáticos de boot volumes (lun/mie/vie)
- Rotación: máximo 5 backups (límite Free Tier)
- Config versionada en este repositorio
