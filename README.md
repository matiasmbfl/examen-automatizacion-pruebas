Automatización de pruebas — Examen final

Repositorio: matiasmbfl/examen-automatizacion-pruebas

Descripción del proyecto

Este proyecto implementa una solución de automatización de pruebas utilizando Java, Maven, JUnit y Selenium. También incluye un pipeline de Integración Continua mediante GitHub Actions y un pipeline de despliegue para un ambiente de pruebas.

La aplicación de ejemplo implementa un servicio que consulta usuarios y genera un saludo personalizado. El objetivo es demostrar la compilación, la ejecución de pruebas automatizadas, la publicación de reportes y un despliegue Blue-Green con rollback.

Estrategia de ramas

Se utiliza Trunk-Based Development:

•
main: rama principal estable.

•
feature/ci-pipeline: rama para configurar el pipeline de integración continua.

•
feature/deployment-blue-green: rama para configurar el despliegue y rollback.

Los cambios se integran a main mediante commits y merges. El pipeline debe terminar correctamente antes de considerar aprobado un cambio.

Estrategia de pruebas

Pruebas unitarias

Validan la lógica de GreetingService de manera aislada.

Archivo:

Plain Text


src/test/java/com/example/automatizacion/GreetingServiceTest.java



Ejecución:

Bash


mvn clean test



Pruebas de integración

Validan la interacción entre GreetingService e InMemoryUserRepository.

Archivo:

Plain Text


src/test/java/com/example/automatizacion/GreetingServiceIT.java



Ejecución:

Bash


mvn clean verify -Pintegration



Pruebas de aceptación

Validan el criterio de negocio: un usuario registrado recibe un saludo personalizado.

Archivo:

Plain Text


src/test/java/com/example/automatizacion/GreetingAcceptanceTest.java



Ejecución:

Bash


mvn clean verify -Pacceptance



Configuración Maven

El archivo pom.xml define las versiones y dependencias del proyecto:

•
JUnit 5 para pruebas unitarias.

•
Selenium Java para futuras pruebas de interfaz.

•
Surefire para pruebas unitarias.

•
Failsafe para pruebas de integración y aceptación.

Comandos principales:

Bash


mvn clean test
mvn clean verify -Pintegration
mvn clean verify -Pacceptance
mvn clean package -DskipTests



Pipeline de Integración Continua

El pipeline está definido en:

Plain Text


.github/workflows/ci.yml



También se incluye un pipeline equivalente para Jenkins en:

Plain Text


Jenkinsfile



Etapas del pipeline

1.
Checkout del código.

2.
Configuración de Java 17.

3.
Build del proyecto.

4.
Pruebas unitarias.

5.
Pruebas de integración.

6.
Acceptance Test Gate.

7.
Despliegue Blue-Green al ambiente de pruebas.

8.
Segundo despliegue Blue-Green en ejecución manual.

9.
Rollback demostrativo en ejecución manual.

10.
Publicación de reportes como artifacts.

El workflow se ejecuta automáticamente con push o Pull Request hacia main. También puede ejecutarse manualmente con Actions → CI y Deployment Pipeline → Run workflow.

Deployment Pipeline

El despliegue utiliza una estrategia Blue-Green:

•
blue: slot de una versión activa.

•
green: slot donde se prepara la siguiente versión.

•
Se valida el artefacto antes de cambiar el slot activo.

•
Si una validación falla, se ejecuta rollback al slot anterior.

Scripts utilizados:

Plain Text


scripts/deploy-test.sh
scripts/rollback.sh



Ejecución local:

Bash


mvn clean package -DskipTests
chmod +x scripts/*.sh
./scripts/deploy-test.sh target/automatizacion-pruebas-1.0.0-SNAPSHOT.jar
./scripts/rollback.sh



Evidencias

Las capturas reales se encuentran en artifacts/screenshots/.

También se incluyen capturas de Git, ramas, pruebas locales, integración y aceptación.

Archivos principales

Archivo o carpeta
Descripción
pom.xml
Configuración Maven y dependencias.
src/main/java
Código de la aplicación de ejemplo.
src/test/java
Pruebas unitarias, de integración y aceptación.
.github/workflows/ci.yml
Pipeline de GitHub Actions.
Jenkinsfile
Pipeline equivalente para Jenkins.
scripts/deploy-test.sh
Despliegue Blue-Green.
scripts/rollback.sh
Rollback al slot anterior.
docs/ejecucion-local.txt
Salida de la ejecución local.
artifacts/screenshots/
Capturas de evidencia.


