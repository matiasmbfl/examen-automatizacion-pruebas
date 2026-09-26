# Automatización de pruebas — Examen final

Proyecto demostrativo para resolver las tres actividades del examen final de **Automatización de Pruebas**. La solución integra control de versiones, Maven, pruebas automatizadas, CI y un deployment pipeline reproducible.

> **Antes de entregar:** reemplaza `[Tu nombre]`, `[Tu apellido]` y `[URL de tu repositorio]`. Las evidencias que se generen localmente pueden adjuntarse como logs; para evidencias de GitHub Actions debes ejecutar el workflow en tu propio repositorio y agregar capturas de la pestaña **Actions**.

## 1. Alcance y estrategia

La aplicación de ejemplo implementa un servicio de saludo que consulta un repositorio de usuarios. Se eligió porque permite demostrar tres niveles de validación sin depender de una API externa:

- **Unitarias:** validan la lógica de `GreetingService` con un repositorio simulado.
- **Integración:** conectan `GreetingService` con `InMemoryUserRepository`.
- **Aceptación:** comprueban el criterio de negocio “un usuario registrado recibe un saludo personalizado”.

Se utiliza **Trunk-Based Development**: `main` es la rama principal protegida; cada cambio se desarrolla en una rama corta `feature/<descripcion>`, se integra mediante Pull Request y el pipeline debe quedar verde antes del merge.

## 2. Estructura

```text
.
├── pom.xml
├── Jenkinsfile
├── .github/workflows/ci.yml
├── src/main/java/.../GreetingService.java
├── src/main/java/.../UserRepository.java
├── src/main/java/.../InMemoryUserRepository.java
├── src/test/java/.../GreetingServiceTest.java       # unitarias
├── src/test/java/.../GreetingServiceIT.java         # integración
├── src/test/java/.../GreetingAcceptanceTest.java       # aceptación
├── scripts/deploy-test.sh                            # Blue-Green a test
├── scripts/rollback.sh                               # rollback al slot anterior
├── deployments/test/                                 # estado local del despliegue
├── docs/                                             # evidencias y notas
└── artifacts/screenshots/                             # capturas para completar
```

## 3. Actividad 1 — Git, ramas y Maven

### Flujo de ramas

```bash
git clone [URL de tu repositorio]
cd examen-automatizacion-pruebas
git switch -c feature/ajuste-pruebas
git add .
git commit -m "feat: configura pruebas automatizadas y pipeline"
git push -u origin feature/ajuste-pruebas
# Abrir Pull Request hacia main; fusionar solo con CI exitoso
```

Los scripts de prueba, los datos, el `pom.xml`, los pipelines y los scripts de despliegue se versionan junto al código. Esto permite conocer qué versión fue probada, reproducir errores y auditar cambios.

### Maven

El archivo `pom.xml` declara versiones explícitas para JUnit 5, Selenium Java, Surefire y Failsafe. Los perfiles separan los tipos de prueba:

```bash
mvn clean test                 # unitarias
mvn clean verify -Pintegration # unitarias + integración
mvn clean verify -Pacceptance  # unitarias + aceptación
```

Selenium está incluido como dependencia de pruebas para dejar el proyecto preparado para una futura prueba UI; la demostración actual utiliza pruebas de servicio deterministas para que el pipeline sea reproducible sin navegador ni servidor externo.

## 4. Actividad 2 — Pipeline de CI

Se incluyen dos alternativas equivalentes:

- `.github/workflows/ci.yml` para GitHub Actions.
- `Jenkinsfile` para Jenkins con agente Maven/JDK 17.

Stages implementados:

1. **Build:** compilación y empaquetado sin ejecutar pruebas.
2. **Pruebas unitarias:** `mvn test`.
3. **Pruebas de integración:** `mvn verify -Pintegration`.
4. **Acceptance Test Gate:** `mvn verify -Pacceptance`.
5. **Deploy to Test — Blue/Green:** publicación del artefacto en un slot alternado.
6. **Rollback:** se ejecuta ante fallo en Jenkins y queda disponible como comando versionado.

Los XML de Surefire/Failsafe y el `.jar` se publican como artefactos del job. En GitHub Actions se descargan desde la sección **Artifacts** de la ejecución; en Jenkins quedan disponibles en **Build Artifacts**.

## 5. Actividad 3 — Deployment pipeline

El script `scripts/deploy-test.sh` alterna entre `deployments/test/blue` y `deployments/test/green`:

1. Comprueba que exista el artefacto.
2. Identifica el slot activo.
3. Copia la nueva versión al slot inactivo.
4. Ejecuta un health check sobre el artefacto y su metadata.
5. Cambia el archivo `deployments/test/active` al nuevo slot.
6. Guarda la última versión exitosa.

Para desplegar:

```bash
mvn -B clean package -DskipTests
chmod +x scripts/*.sh
./scripts/deploy-test.sh target/automatizacion-pruebas-1.0.0-SNAPSHOT.jar
```

Para revertir al slot anterior:

```bash
./scripts/rollback.sh
cat deployments/test/active
cat deployments/test/last-successful
```

La elección **Blue-Green** permite cambiar de versión sin modificar gradualmente el tráfico y hace que el rollback sea una conmutación simple al slot anterior. En un ambiente real, el archivo `active` se reemplazaría por el switch del balanceador o Service/Ingress de Kubernetes.

## 6. Evidencias

La ejecución local se registra en `docs/evidencia-ejecucion.md`. Para la entrega académica, agrega capturas en `artifacts/screenshots/` de:

- Repositorio y ramas en GitHub.
- `pom.xml` y estructura del proyecto.
- Ejecución verde de los stages en GitHub Actions o Jenkins.
- Reportes de pruebas unitarias e integración.
- Despliegue al slot Blue/Green y ejecución del rollback.

**No presentes como captura real una imagen simulada.** Si trabajas solo localmente, entrega los logs reproducibles y una captura de la terminal; si el docente exige GitHub, ejecuta el workflow en tu repositorio y toma las capturas desde allí.

## 7. Matriz de cumplimiento

| Requisito | Implementación | Evidencia |
|---|---|---|
| Repositorio Git y flujo de ramas | `main` protegida + `feature/*` + PR | GitHub y `git log` |
| Proyecto Maven | `pom.xml` con JUnit, Selenium, Surefire/Failsafe | `pom.xml`, `mvn test` |
| Build CI | Stage `Build` | log del workflow |
| Pruebas unitarias | `GreetingServiceTest` | Surefire XML |
| Pruebas de integración | `GreetingServiceIT` + perfil `integration` | Failsafe XML |
| Acceptance tests | `GreetingAcceptanceTest` + perfil `acceptance` | Failsafe XML |
| Despliegue en test | `scripts/deploy-test.sh` | `DEPLOYMENT_OK` |
| Rollback | `scripts/rollback.sh` | `ROLLBACK_OK` |
| Documentación | este README y `docs/evidencia-ejecucion.md` | archivos versionados |

## 8. Referencias de los materiales de apoyo

- ME_1: Git, estrategias de ramificación, Maven, POM y ciclo de vida.
- ME_2: administración de configuración, líneas base, trazabilidad y ambientes reproducibles.
- ME_3: CI, stages, artefactos, reportes e integración de pruebas.
- ME_5: deployment pipeline, commit stage y Acceptance Test Gate.
- ME_6: rollback, Blue-Green/Canary, recuperación y auditoría.
- R_3/R_4: estructura de entregables, reportes y evidencias de ejecución.
