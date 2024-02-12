
# API de Simulación de Hipoteca

## Descripción del Proyecto

Este proyecto es una API de simulación de hipoteca diseñada para calcular estimaciones de préstamos hipotecarios. Puede ser utilizada de manera rápida y sencilla para estimar sus pagos hipotecarios mensuales y totales.

## Documentación

La documentación completa de la API se encuentra disponible en [Postman](https://documenter.getpostman.com/view/18479792/2s9YytggMg). En ella, encontrará información detallada sobre los endpoints disponibles, los parámetros de solicitud, los ejemplos de respuestas y cómo utilizar la API en sus aplicaciones.

## Funcionalidades Principales

- **Crear Cliente**: Registre nuevos clientes con información como nombre, DNI, correo electrónico y capital solicitado.

- **Obtener Detalles del Cliente**: Consulte la información de un cliente específico proporcionando su número de DNI.

- **Eliminar Cliente**: Elimine a un cliente registrando su número de DNI.

- **Actualizar Detalles del Cliente**: Actualice la información de un cliente existente utilizando su número de DNI.

- **Simulación de Hipoteca**: Realice simulaciones de préstamos hipotecarios proporcionando la TAE (Tasa Anual Equivalente) y el plazo de amortización.

## Uso

1. Clone el repositorio en su máquina local:

```bash
git clone https://github.com/jakynevs/mortgage_sim
```

2. Instale las dependencias necesarias:

```bash
pip install -r requirements.txt
```

3. Configuración de la Base de Datos:

Antes de ejecutar la aplicación, asegúrese de configurar la base de datos. Hay dos scripts importantes para preparar su entorno de base de datos:

- **db_setup.py**: Utilice este script para crear el esquema de la base de datos.
- **populate_db.py**: Este script poblara la base de datos con datos de prueba iniciales.

**Importante**: Deberá modificar el nombre de la base de datos en ambos scripts (db_setup.py y populate_db.py) dependiendo de sus preferencias y entorno.

4. Ejecute la aplicación:

```bash
python app.py
```

5. Acceda a la API a través de la siguiente URL local:

```bash
http://localhost:5000
```

