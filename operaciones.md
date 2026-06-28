# ⚙️ Procedimientos Operativos

## Cómo conectarse a cada máquina

### Desde PC (Victus)
```bash
# A main (Ticia)
ssh ubuntu@100.109.36.3

# A monitor-1 (Mia)
ssh ubuntu@100.73.29.14

# A monitor-2 (Cline)
ssh ubuntu@100.68.19.107
```

### Desde celular (Termux)
```bash
pkg install openssh -y
ssh ubuntu@100.73.29.14     # Mia
ssh ubuntu@100.68.19.107    # Cline
ssh ubuntu@100.109.36.3     # Ticia (main)
```

## Cómo reiniciar cada agente

### Ticia (main)
```bash
ssh ubuntu@100.109.36.3
sudo systemctl restart openclaw-ticia
```

### Mia (monitor-1)
```bash
ssh ubuntu@100.73.29.14
sudo systemctl restart goose-mia
```

### Cline (monitor-2)
```bash
ssh ubuntu@100.68.19.107
sudo systemctl restart goose
```

### Claw, Lina, Gemma (Docker)
```bash
ssh ubuntu@100.109.36.3
docker restart moltbot-clawdbot-1
```

## Cómo generar pairing codes (Goose)

Cuando un bot Goose se reinicia, puede pedir un pairing code para vincularse al chat de Telegram.

```bash
# En monitor-1 (Mia)
ssh ubuntu@100.73.29.14
/home/ubuntu/.local/bin/goose gateway pair telegram

# En monitor-2 (Cline)
ssh ubuntu@100.68.19.107
/home/ubuntu/.local/bin/goose gateway pair telegram
```

## Cómo ver logs

### Ticia (main)
```bash
journalctl -u openclaw-ticia --no-pager -n 50
tail -50 /var/log/openclaw-ticia.log
```

### Mia (monitor-1)
```bash
journalctl -u goose-mia --no-pager -n 50
```

### Cline (monitor-2)
```bash
journalctl -u goose --no-pager -n 50
```

### Docker
```bash
docker logs moltbot-clawdbot-1 --tail 50
docker exec moltbot-clawdbot-1 cat /tmp/openclaw/openclaw-2026-06-28.log
```

## Procedimiento de recuperación

### Si main se cae

1. Conectarse a **monitor-1** (Mia) o **monitor-2** (Cline) por SSH
2. Diagnosticar: `ssh main "uptime && free -m && docker ps"`
3. Si main está reachable pero los agentes no responden:
   ```bash
   ssh main "sudo systemctl restart openclaw-ticia"
   ssh main "docker restart moltbot-clawdbot-1"
   ```
4. Si main no responde, revisar desde la consola OCI

### Si un bot Goose se cae
```bash
ssh monitor "sudo systemctl restart goose-mia"  # o goose
# Si pide pairing code:
ssh monitor "goose gateway pair telegram"
```

### Si un agente Docker no responde
```bash
ssh main
docker logs moltbot-clawdbot-1 --tail 20
docker restart moltbot-clawdbot-1
```

### Si se pierde una API key de OpenRouter
1. Ir a https://openrouter.ai/keys
2. Crear nueva key
3. Actualizar en el servicio correspondiente:
   - **Ticia:** actualizar OPENROUTER_API_KEY y reiniciar gateway
   - **Mia/Cline:** actualizar en secrets.yaml y reiniciar servicio
   - **Docker:** actualizar env var y reiniciar contenedor

## Backup y restauración

### Backup de configs
```bash
# OpenClaw configs
cp /root/.openclaw-ticia/openclaw.json /root/.openclaw-ticia/openclaw.json.bak.$(date +%Y%m%d)

# Goose configs (en cada monitor)
cp ~/.config/goose/config.yaml ~/.config/goose/config.yaml.bak.$(date +%Y%m%d)
```

### Restauración desde backup de boot volume
1. Ir a OCI Console → Block Storage → Boot Volume Backups
2. Seleccionar el backup más reciente
3. Crear instancia desde backup
4. Reconfigurar Tailscale y claves SSH
5. Levantar los servicios
