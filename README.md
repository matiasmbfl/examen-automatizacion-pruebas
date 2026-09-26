# Automatización de pruebas — Examen final

## Descripción del proyecto

Este proyecto implementa una solución de automatización de pruebas utilizando Java, Maven, JUnit y Selenium. Además, incluye un pipeline de Integración Continua mediante GitHub Actions y un pipeline de despliegue para un ambiente de pruebas.

La aplicación de ejemplo implementa un servicio que consulta usuarios y genera un saludo personalizado.

## Estrategia de pruebas implementada

Se implementaron los siguientes tipos de pruebas:

### Pruebas unitarias

Validan la lógica interna del servicio de manera aislada.

Archivo:

```text
src/test/java/com/example/automatizacion/GreetingServiceTest.java
