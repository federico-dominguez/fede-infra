# 🔐 Seguridad y Accesos

## Principios

- **Zero Trust:** No hay puertos SSH abiertos al mundo
- **Defensa en profundidad:** Tailscale VPN + claves SSH + security lists
- **Keys independientes:** Cada agente tiene su propia API key de OpenRouter

## Acceso SSH

Todas las conexiones SSH se realizan **exclusivamente por Tailscale**.

### Hosts y direcciones

| Máquina | IP Tailscale | Usuario SSH | Alias |
|---------|-------------|-------------|-------|
| **main** | `100.109.36.3` | `ubuntu` | `ssh main` |
| **monitor-1** | `100.73.29.14` | `ubuntu` | `ssh monitor-1` |
| **monitor-2** | `100.68.19.107` | `ubuntu` | `ssh monitor-2` |
| **victus** (PC Fede) | `100.85.243.10` | `fede` | `tailscale ssh victus` |

### Claves autorizadas

| Clave | Dueño | Instancias |
|-------|-------|------------|
| `ticia@openclaw-vps` (ed25519) | Ticia (main) | main, monitor-1, monitor-2 |
| `openclaw-vps` (ed25519) | Fede (PC) | main, monitor-1, monitor-2 |
| `fede-android` (ed25519 desde Termux) | Fede (celular) | main, monitor-1, monitor-2 |

### SSH Config (con alias)

```bash
Host main
  HostName 100.109.36.3
  User ubuntu

Host monitor-1
  HostName 100.73.29.14
  User ubuntu

Host monitor-2
  HostName 100.68.19.107
  User ubuntu
```

## Seguridad de red OCI

| Puerto | Servicio | Acceso | Estado |
|--------|----------|--------|--------|
| 22 | SSH | `0.0.0.0/0` | 🔴 CERRADO (solo por Tailscale) |
| 80 | HTTP | `0.0.0.0/0` | 🟢 Abierto |
| 443 | HTTPS | `0.0.0.0/0` | 🟢 Abierto |
| 18789 | ? | `0.0.0.0/0` | 🔴 CERRADO |

## Tailscale

- **Tailnet:** `.tail5516d3.ts.net`
- **SSH:** Activado en victus (PC de Fede)
- **Auth:** Clave de autenticación reusable

## IAM OCI

- **Dynamic Group:** `openclaw-instances` (incluye las 3 instancias)
- **Policy:** `Allow dynamic-group openclaw-instances to manage all-resources in tenancy`
- **API Keys:** Ninguna. Autenticación via Instance Principals.

## Respaldo de accesos

En caso de pérdida total de acceso:

1. **Consola OCI:** https://cloud.oracle.com (usuario: sdominguez.federico@gmail.com)
2. **Tailscale:** https://login.tailscale.com (para aprobar conexiones SSH)
3. **OpenRouter:** https://openrouter.ai/keys (para regenerar API keys)
4. **Telegram:** Los bots están en @s_ticia_bot, @s_clawopen_bot, @s_lina_bot, @s_gemma_bot
