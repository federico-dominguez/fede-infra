# 🤖 Mapa de Agentes

## Agentes OpenClaw (nativos y Docker)

### 🐱 Ticia (main)
| Atributo | Valor |
|----------|-------|
| **Tipo** | OpenClaw nativo (ARM64) |
| **Host** | main (100.109.36.3) |
| **Modelo** | `openrouter/deepseek/deepseek-v4-pro` |
| **API Key** | `main-key` (sk-or-…60d4) |
| **Puerto** | 47718 |
| **Rol** | Agente principal. Orquesta todo, ejecuta tareas complejas, gestiona infraestructura. |

### 🐶 Claw (Docker)
| Atributo | Valor |
|----------|-------|
| **Tipo** | OpenClaw en Docker |
| **Bot Telegram** | @s_clawopen_bot |
| **Modelo** | `deepseek/deepseek-v4-pro` |
| **API Key** | `main-moltbot-key` |
| **Rol** | Agente de propósito general dentro del Docker. Ejecuta tareas, responde consultas. |

### 🧘 Lina (Docker)
| Atributo | Valor |
|----------|-------|
| **Tipo** | OpenClaw en Docker |
| **Bot Telegram** | @s_lina_bot |
| **Modelo** | `deepseek/deepseek-v4-flash` |
| **API Key** | `main-moltbot-key` |
| **Rol** | Agente de bienestar personal. Pregunta cómo estuvo el día, registra emociones, da apoyo. |

### 💎 Gemma (Docker)
| Atributo | Valor |
|----------|-------|
| **Tipo** | OpenClaw en Docker |
| **Bot Telegram** | @s_gemma_bot |
| **Modelo** | `deepseek/deepseek-v4-flash` |
| **API Key** | `main-moltbot-key` |
| **Rol** | Agente adicional dentro del Docker. |

## Agentes Goose (guardianes)

### 👀 Mia (monitor-1)
| Atributo | Valor |
|----------|-------|
| **Tipo** | Goose v1.39.0 |
| **Host** | monitor-1 (100.73.29.14) |
| **Modelo** | `deepseek/deepseek-v4-flash` |
| **API Key** | `monitor-1-key` (sk-or-…9603) |
| **Personalidad** | Hermana cariñosa, monitorea main cada 30 min. |
| **Servicio** | `goose-mia.service` |
| **Rol** | **Guardia #1.** Reporta estado de main. Puerta de entrada si main falla. |

### 🐶 Cline (monitor-2)
| Atributo | Valor |
|----------|-------|
| **Tipo** | Goose v1.39.0 |
| **Host** | monitor-2 (100.68.19.107) |
| **Modelo** | `deepseek/deepseek-v4-flash` |
| **API Key** | `monitor-2-key` (sk-or-…8930) |
| **Personalidad** | Hermano reservado. Solo habla si hay problemas. Backup de Mia. |
| **Servicio** | `goose.service` |
| **Rol** | **Guardia #2.** Backup de Mia. Silencioso, solo alerta si algo anda mal. |

## Matriz de roles

| Quién | Tipo | Rol | Proactivo | Modelo |
|-------|------|-----|-----------|--------|
| Ticia | OpenClaw | Principal | Sí (cron) | Pro |
| Claw | OpenClaw (Docker) | Propósito general | No | Pro |
| Lina | OpenClaw (Docker) | Bienestar | Sí (cron) | Flash |
| Gemma | OpenClaw (Docker) | Propósito general | No | Flash |
| Mia | Goose | Guardia #1 | Sí (cada 30 min) | Flash |
| Cline | Goose | Guardia #2 | No (solo alerta) | Flash |
