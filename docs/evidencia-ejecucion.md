# Evidencia de ejecución

> Este archivo se completa con la salida obtenida al ejecutar los comandos. Las capturas de GitHub Actions/Jenkins deben tomarse del sistema realmente utilizado.

## Actividad 1 — Git y Maven

```text
[PEGAR AQUÍ: git branch -a]
[PEGAR AQUÍ: git log --oneline --decorate --graph -n 10]
[PEGAR AQUÍ: mvn -version]
```

## Actividad 2 — CI

```text
[PEGAR AQUÍ: mvn -B clean test]
[PEGAR AQUÍ: mvn -B verify -Pintegration]
[PEGAR AQUÍ: mvn -B verify -Pacceptance]
```

Capturas sugeridas:

- `artifacts/screenshots/01-repositorio-y-ramas.png`
- `artifacts/screenshots/02-build-y-pruebas-verdes.png`
- `artifacts/screenshots/03-reportes-de-pruebas.png`

## Actividad 3 — Deployment y rollback

```text
[PEGAR AQUÍ: salida de ./scripts/deploy-test.sh ...]
[PEGAR AQUÍ: salida de ./scripts/rollback.sh]
```

Capturas sugeridas:

- `artifacts/screenshots/04-deploy-blue-green.png`
- `artifacts/screenshots/05-rollback-ok.png`

## Interpretación

Un resultado verde en build, pruebas unitarias, integración y aceptación habilita el despliegue al ambiente de prueba. Si una validación falla, el pipeline debe detenerse y conservar logs. El rollback restaura el slot anterior y deja trazabilidad de la versión activa.
