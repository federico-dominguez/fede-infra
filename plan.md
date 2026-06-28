# 🗺️ Plan de Desarrollo

## Visión general

Construir un **ecosistema de agentes personales** que automaticen tareas de infraestructura, desarrollo, bienestar y proyectos universitarios — todo desde Oracle Cloud Free Tier.

## Fases

### ✅ Fase 1 — Fundación (COMPLETADA)
- [x] 3 VPS en Oracle Cloud
- [x] Tailscale en todas (VPN zero-trust)
- [x] SSH cerrado al mundo
- [x] Dynamic Group + OCI API
- [x] Nomenclatura clara (main, monitor-1, monitor-2)
- [x] Documentación viva en `docs/`

### 🟡 Fase 2 — Automatización (EN PROGRESO)

#### Prioridad Alta
- [ ] **ML Browser Scraping** — login manual + scraping de precios
- [ ] **Monitor-2 (Cline)** — schedule nativo de Goose funcional
- [ ] **Lina proactiva** — que no solo responda, que ella inicie conversaciones fuera del cron

#### Prioridad Media
- [ ] **Keys separadas para Docker** — Ticia, Claw, Lina, Gemma cada una con su propia key de OpenRouter
- [ ] **Monitoreo de keys** — script que verifique cada hora que las API keys de OpenRouter respondan
- [ ] **Alertas reales** — si Mia no responde, que Cline alerte. Si Cline no responde, que alerte Ticia.

### 🔵 Fase 3 — Pipeline de desarrollo (PRÓXIMA)

#### Agentes para sinep
- [ ] Contenedor Docker dedicado con el repo de sinep clonado
- [ ] **4 agentes especializados**:
  - 🤖 **Planificador** — analiza issues, define tareas
  - 🤖 **Implementador** — escribe código, corre tests
  - 🤖 **Revisor** — hace code review, busca bugs
  - 🤖 **Deployer** — build, test, deploy a staging
- [ ] Pipeline secuencial: `Plan → Code → Test → Review → Fix → Review → Deploy`

### 🟢 Fase 4 — Ecosistema (FUTURO)

- [ ] Dashboard web con estado de todos los agentes
- [ ] Historial de conversaciones centralizado
- [ ] Agente para cada proyecto personal
- [ ] Automatización de facturas, recordatorios, calendario
- [ ] Integración con servicios externos (Gmail, Drive, calendario)

## Roadmap semanal

### Semana 1 (actual)
| Día | Tarea |
|-----|-------|
| ✅ Sábado | Infraestructura base (COMPLETADO) |
| ⬜ Domingo (mañana) | ML Browser scraping funcional |
| ⬜ Domingo (tarde) | Pipeline sinep: diseño de agentes |
| ⬜ Lunes | Implementar pipeline sinep |
| ⬜ Martes | Monitoreo de keys + alertas |
| ⬜ Miércoles | Separar keys de Docker |
| ⬜ Jueves | Dashboard web |
| ⬜ Viernes | Bug fixes + documentación |

## Principios de operación

1. **Un cambio por vez** — probar en monitor-1/2 antes de tocar main
2. **Backup antes de editar** — siempre guardar config antes de modificar
3. **Documentar al hacer** — no dejar la documentación para después
4. **Nada crítico sin probar** — los cambios grandes se prueban en monitor primero
5. **Si se rompe, se revive** — tenemos procedimientos de recuperación
