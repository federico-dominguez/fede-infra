# 🖥️ Dashboard Fede — Oracle + OpenRouter

Dashboard profesional y sencillo para monitorear la instancia Oracle Cloud y el consumo de OpenRouter,
accesible solo desde la red privada de [Tailscale](https://tailscale.com/).

## Stack

| Componente | Tecnología |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + uvicorn |
| Métricas sistema | [psutil](https://github.com/giampaolo/psutil) |
| API externa | [httpx](https://www.python-httpx.org/) → OpenRouter API |
| Frontend | HTML + CSS vanilla (sin frameworks JS) |
| Red privada | Tailscale (puerto 8080) |

## Endpoints

| Ruta | Descripción |
|---|---|
| `GET /` | Dashboard HTML con datos server-side |
| `GET /api/system` | JSON: CPU%, RAM%, disco%, uptime, IPs |
| `GET /api/openrouter` | JSON: créditos cuenta + consumo por key |

## Instalación

```bash
# 1. Clonar el repo
git clone https://github.com/federico-dominguez/fede-infra.git
cd fede-infra/dashboard

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar environment
export OPENROUTER_API_KEY="sk-or-v1-..."
export CLAW_OPENROUTER_API_KEY="sk-or-v1-..."

# 4. Iniciar
python3 server.py

# 5. Abrir en el navegador
#    http://<TAILSCALE_IP>:8080
```

## Systemd (auto-arranque)

```bash
cp dashboard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now dashboard
```

## Datos que muestra

### 🖥️ Servidor Oracle
- **Name:** `main`
- **IP:** Tailscale + interfaces
- **CPU:** % con gauge
- **RAM:** GB usado/total + % gauge
- **Disco:** GB usado/total + % gauge
- **Uptime**
- **Backup:** on/off

### 🔑 OpenRouter
- Créditos totales de la cuenta
- Consumo por key (`main` / `main-moltbot`)
- Créditos restantes
- Alertas visuales si créditos bajos (< $1 rojo, < $5 amarillo)

## Estructura

```
dashboard/
├── server.py              # FastAPI app
├── templates/
│   └── dashboard.html     # HTML con CSS inline
├── requirements.txt       # Dependencias pip
├── dashboard.service      # systemd unit
└── README.md              # Este archivo
```

## Notas de seguridad

- El dashboard solo escucha en la IP de Tailscale.
- Sin autenticación adicional — la seguridad la da la red privada.
- Las API keys se pasan por environment variables, no están hardcodeadas.

---

Hecho con ❤️ por Lena 🐱‍👤 para Fede
