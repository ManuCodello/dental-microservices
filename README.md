# Odontología — Microservicios (Flask + JWT)

Este repositorio contiene un ejemplo didáctico de microservicios desarrollados con Flask y protegidos mediante JWT. Incluye un API Gateway que enruta las solicitudes a 5 microservicios independientes.

## Arquitectura

- API Gateway — puerto 5000
- Pacientes — puerto 5001
- Consultas — puerto 5002
- Facturación — puerto 5003
- Seguimiento — puerto 5004
- Notificaciones — puerto 5005

Cada microservicio contiene los archivos principales: `app.py`, `routes.py`, `models.py`, `utils.py`.

## Requisitos

- Python 3.10 o superior
- pip

Es recomendable usar un entorno virtual para instalar dependencias.

## Instalación rápida

1. Clona el repositorio o descarga el código.

2. Crea y activa un entorno virtual.

PowerShell (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala dependencias desde la raíz del proyecto:

```powershell
pip install -r requirements.txt
```

## Variables de entorno

- El API Gateway incluye un archivo de ejemplo `.env.example` en `api_gateway/`.
- La variable principal es `CLAVE_SECRETA` (utilizada para firmar JWT). Si no se define, los servicios pueden usar un valor por defecto interno.
- No subas tu `.env` real al repositorio. `.gitignore` ya excluye `.env` y archivos `*.db`.

## Ejecutar los servicios (modo manual)

Abre una terminal por cada servicio y ejecuta el siguiente comando desde la carpeta del servicio correspondiente.

Ejemplo (PowerShell):

```powershell
# En una terminal por servicio:
cd api_gateway
python app.py
```

```powershell
cd pacientes
python app.py
```

```powershell
cd consultas
python app.py
```

```powershell
cd facturacion
python app.py
```

```powershell
cd seguimiento
python app.py
```

```powershell
cd notificaciones
python app.py
```

Cada aplicación por defecto arranca en el puerto indicado en la sección "Arquitectura".

Nota: si prefieres automatizar el arranque en Windows PowerShell puedes crear un script que abra varias ventanas y ejecute cada servicio (esto depende de tu flujo de trabajo). Para desarrollo local, varias pestañas de terminal funcionan bien.

## Generar un token JWT de prueba

El API Gateway ofrece un endpoint para obtener un token de prueba (ver `api_gateway/routes.py` si necesitas adaptar los datos de usuario):

Ejemplo de petición (curl):

```bash
curl -X POST http://localhost:5000/auth/token -H "Content-Type: application/json" -d '{"usuario":"demo"}'
```

Respuesta esperada:

```json
{ "token": "<JWT>" }
```

Usa ese token en la cabecera `Authorization: Bearer <JWT>` al consumir los endpoints protegidos.

## Endpoints de ejemplo (vía API Gateway)

- Crear paciente

  POST http://localhost:5000/pacientes/pacientes
  Headers: Authorization: Bearer <JWT>, Content-Type: application/json

  Body ejemplo:
  ```json
  { "nombre": "Juan Perez", "edad": 30 }
  ```

- Listar pacientes

  GET http://localhost:5000/pacientes/pacientes
  Headers: Authorization: Bearer <JWT>

- Listar consultas

  GET http://localhost:5000/consultas/consultas
  Headers: Authorization: Bearer <JWT>

- Crear factura

  POST http://localhost:5000/facturacion/facturas
  Headers: Authorization: Bearer <JWT>, Content-Type: application/json

  Body ejemplo:
  ```json
  { "paciente_id": 1, "monto": 1500.0, "estado": "pendiente" }
  ```

## Notas y recomendaciones

- Cada microservicio crea su propia base de datos SQLite en el primer arranque.
- Este proyecto es una base para aprendizaje. Para producción considera añadir: pruebas automatizadas, logging centralizado, health checks, contenedores (Docker), y orquestación.

## Siguientes pasos sugeridos

- Añadir un script de arranque (PowerShell o Makefile) para ejecutar todos los servicios en desarrollo.
- Añadir tests unitarios e integración para los endpoints principales.
- Contenerizar cada servicio con Docker y preparar un docker-compose para desarrollo.

---

