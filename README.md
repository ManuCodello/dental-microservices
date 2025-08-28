# Odontología Microservicios (Flask + JWT)

Proyecto de referencia estilo MVC simplificado, con 5 microservicios independientes y un API Gateway. Cada servicio es una app Flask con su propia base de datos SQLite y validación por JWT. Arquitectura simple, escalable y con nombres/variables en español.

## Arquitectura

- API Gateway (puerto 5000)
- Pacientes (5001)
- Consultas (5002)
- Facturación (5003)
- Seguimiento (5004)
- Notificaciones (5005)

Cada microservicio incluye: `app.py`, `routes.py`, `models.py`, `utils.py`.

## Requisitos

- Python 3.10+
- Pip

## Instalación

1) Clonar o copiar el proyecto.

2) Crear y activar un entorno virtual (opcional pero recomendado):

- Windows (PowerShell):
```
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```
- Linux/Mac:
```
python3 -m venv .venv
source .venv/bin/activate
```

3) Instalar dependencias en la raíz del proyecto:
```
pip install -r requirements.txt
```

4) Variables de entorno

- El API Gateway incluye un `.env` con `CLAVE_SECRETA` de ejemplo. Puedes cambiarla en `odontologia_microservicios/api_gateway/.env`.
- Los microservicios leen la variable `CLAVE_SECRETA` del entorno si existe; si no, usan un valor por defecto (`super_secreto`).

## Ejecución

Abre 6 terminales (una por servicio) y ejecuta en cada carpeta el siguiente comando:

- API Gateway
```
python app.py
```

- Pacientes
```
python app.py
```

- Consultas
```
python app.py
```

- Facturación
```
python app.py
```

- Seguimiento
```
python app.py
```

- Notificaciones
```
python app.py
```

Nota: Ejecuta cada comando dentro de la carpeta correspondiente (`api_gateway/`, `pacientes/`, `consultas/`, `facturacion/`, `seguimiento/`, `notificaciones/`).

## Generar token JWT de prueba

El API Gateway expone un endpoint para emitir un token de prueba:

```
POST http://localhost:5000/auth/token
Content-Type: application/json

{
  "usuario": "demo"
}
```

Respuesta:
```
{
  "token": "<JWT>"
}
```

## Probar endpoints (vía Gateway)

- Crear paciente:
```
POST http://localhost:5000/pacientes/pacientes
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "nombre": "Juan Perez",
  "edad": 30
}
```

- Listar pacientes:
```
GET http://localhost:5000/pacientes/pacientes
Authorization: Bearer <JWT>
```

- Listar consultas:
```
GET http://localhost:5000/consultas/consultas
Authorization: Bearer <JWT>
```

- Crear factura:
```
POST http://localhost:5000/facturacion/facturas
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "paciente_id": 1,
  "monto": 1500.0,
  "estado": "pendiente"
}
```

## Notas

- Las bases de datos SQLite se crean automáticamente en el primer arranque de cada microservicio.
- `.gitignore` excluye `.env` y `*.db`.
- Este proyecto es didáctico; para producción considera: logging centralizado, health checks, rate limiting, retries, circuit breaker, monitorización, y despliegue contenedorizado.
