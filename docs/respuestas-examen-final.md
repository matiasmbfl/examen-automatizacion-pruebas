# Automatización de pruebas — Examen final

**Estudiante:** [Completar nombre y apellido]  
**Asignatura:** Automatización de Pruebas  
**Proyecto:** `automatizacion-pruebas`  
**Estrategia de ramas:** Trunk-Based Development  
**Fecha:** [Completar fecha]

## Introducción

La solución implementa un proyecto Maven con pruebas unitarias, de integración y de aceptación; un pipeline de integración continua versionado; y un deployment pipeline para un ambiente de pruebas con estrategia Blue-Green y rollback. Se eligió una aplicación de ejemplo pequeña y determinista para que las pruebas puedan ejecutarse sin depender de servicios externos.

El servicio bajo prueba (`GreetingService`) consulta un repositorio de usuarios y genera un saludo personalizado. La separación por niveles permite demostrar el flujo completo: la lógica se valida aisladamente, luego se integra con un repositorio en memoria y finalmente se verifica un criterio de negocio.

## Actividad 1 — Repositorio Git y proyecto Maven

### Flujo de ramas

Se utiliza **Trunk-Based Development**. La rama `main` representa la línea principal estable y se mantiene protegida. Cada cambio se desarrolla en una rama corta con el formato `feature/<descripcion>`, se revisa mediante Pull Request y solo se integra cuando el pipeline queda verde.

Ejemplo:

```bash
git switch -c feature/ajuste-pruebas
git add .
git commit -m "feat: configura pruebas automatizadas y pipeline"
git push -u origin feature/ajuste-pruebas
```

Esta estrategia favorece commits frecuentes, integración temprana, trazabilidad y menor divergencia entre ramas. El código de producción, los tests, `pom.xml`, los pipelines y los scripts de despliegue permanecen bajo control de versiones.

### Estructura Maven

```text
src/main/java/.../GreetingService.java
src/main/java/.../UserRepository.java
src/main/java/.../InMemoryUserRepository.java
src/test/java/.../GreetingServiceTest.java
src/test/java/.../GreetingServiceIT.java
src/test/java/.../GreetingAcceptanceTest.java
pom.xml
```

El archivo `pom.xml` define versiones explícitas de Java 17, JUnit 5, Selenium Java, Surefire y Failsafe. Selenium se incluye como dependencia de pruebas para dejar preparada una futura validación UI, mientras que la demostración actual es determinista y no requiere un navegador externo.

Comandos principales:

```bash
mvn clean test
mvn clean verify -Pintegration
mvn clean verify -Pacceptance
```

El primer comando ejecuta pruebas unitarias; el perfil `integration` agrega las pruebas `*IT.java`; y el perfil `acceptance` agrega las pruebas `*AcceptanceTest.java`. Surefire y Failsafe generan reportes XML para que el servidor CI pueda publicarlos.

## Actividad 2 — Pipeline de integración continua

Se entregan dos archivos equivalentes:

- `.github/workflows/ci.yml`, para GitHub Actions.
- `Jenkinsfile`, para Jenkins con un agente Maven/JDK 17.

### Stages

| Stage | Comando o acción | Propósito |
|---|---|---|
| Build | `mvn clean package -DskipTests` | Compilar y generar el artefacto |
| Unit Tests | `mvn test` | Validar lógica aislada rápidamente |
| Integration Tests | `mvn verify -Pintegration` | Validar interacción entre servicio y repositorio |
| Acceptance Test Gate | `mvn verify -Pacceptance` | Validar el criterio de negocio crítico |
| Deploy to Test | `scripts/deploy-test.sh` | Publicar el artefacto en un ambiente de prueba |
| Rollback | `scripts/rollback.sh` | Restaurar el slot anterior si una etapa falla |

El workflow se activa con `push`, Pull Request hacia `main` y ejecución manual. Los reportes `target/surefire-reports/`, `target/failsafe-reports/` y el `.jar` se publican como artefactos de la ejecución. En Jenkins, `junit` registra los resultados y `archiveArtifacts` conserva los reportes y el paquete.

La solución aplica el principio **fail fast**: la compilación y las pruebas se ejecutan antes del despliegue. Si una etapa falla, el pipeline no debe promover la versión y Jenkins ejecuta el rollback documentado.

## Actividad 3 — Deployment pipeline y recuperación

El deployment pipeline transforma el artefacto Maven en una versión desplegable y lo entrega al ambiente de pruebas después de superar el Acceptance Test Gate.

### Despliegue Blue-Green

El script `scripts/deploy-test.sh` mantiene dos slots:

- `blue`: versión estable o activa.
- `green`: versión nueva preparada para validación.

En cada ejecución se identifica el slot activo, se publica la nueva versión en el slot inactivo, se comprueban el artefacto y su metadata, y se cambia el archivo `deployments/test/active` al nuevo slot. En una infraestructura real, este cambio equivaldría a actualizar el Service, Ingress o balanceador.

### Rollback

El script `scripts/rollback.sh` identifica el slot activo y vuelve al slot anterior. Los scripts están versionados y el procedimiento es reproducible:

```bash
./scripts/rollback.sh
```

Blue-Green fue seleccionado porque el proyecto es pequeño y necesita una demostración clara de recuperación sin modificar gradualmente el tráfico. En producción, esta estrategia requiere dos ambientes equivalentes y compatibilidad del esquema de datos; sus ventajas son el cambio rápido y un rollback sencillo.

## Evidencia de ejecución

La validación local se realizó con Java 17 y Maven 3.8.7. Resultados observados:

| Validación | Resultado |
|---|---:|
| Pruebas unitarias | 2 ejecutadas, 0 fallas |
| Pruebas de integración | 1 ejecutada, 0 fallas |
| Pruebas de aceptación | 1 ejecutada, 0 fallas |
| Build del artefacto | `BUILD SUCCESS` |
| Primer despliegue | `DEPLOYMENT_OK`, slot `blue` |
| Segundo despliegue | `DEPLOYMENT_OK`, slot `green` |
| Rollback | `ROLLBACK_OK`, retorno a `blue` |

La salida completa queda en `docs/ejecucion-local.txt`. Para cumplir la exigencia de capturas del docente, se deben agregar al directorio `artifacts/screenshots/` capturas reales de GitHub Actions o Jenkins, del repositorio y de la terminal local.

## Conclusión

La solución articula Git, Maven, pruebas automatizadas, CI y deployment pipeline en un flujo trazable y reproducible. Las validaciones rápidas detectan errores antes de invertir recursos en el despliegue; el Acceptance Test Gate evita promover versiones que no cumplen el criterio de negocio; y Blue-Green con rollback reduce el impacto de una versión defectuosa.

## Referencias de los materiales entregados

- ME_1: Git, estrategias de ramificación, Maven, POM y ciclo de vida.
- ME_2: administración de configuración, líneas base, trazabilidad y ambientes reproducibles.
- ME_3: integración continua, stages, artefactos, reportes y suites de pruebas.
- ME_5: deployment pipeline, etapa de commit y Acceptance Test Gate.
- ME_6: rollback, Blue-Green/Canary, recuperación, seguridad y auditoría.
- R_3 y R_4: estructura sugerida de entregables, reportes y evidencias.
