# Nota técnica de solución

## Decisiones

1. **Trunk-Based Development:** reduce divergencia entre ramas y favorece integración frecuente mediante Pull Requests.
2. **Maven:** centraliza versiones y dependencias en `pom.xml`; los perfiles separan unitarias, integración y aceptación.
3. **Fail fast:** las validaciones rápidas se ejecutan antes del despliegue.
4. **Acceptance Gate:** el despliegue no debe continuar si el criterio de negocio no se cumple.
5. **Blue-Green:** mantiene un slot anterior disponible para cambiar de vuelta rápidamente.
6. **Trazabilidad:** cada etapa produce logs y reportes; los scripts y pipelines se versionan junto al código.

## Limitación explícita

La demostración de despliegue es local y no representa un clúster real. Para una entrega con evidencia de infraestructura real, el mismo patrón puede implementarse con dos deployments Kubernetes y un Service/Ingress que cambie el selector o el peso del tráfico. Esta solución no inventa capturas de GitHub; deja comandos y rutas para obtenerlas de forma reproducible.
