
# API de Simulación de Hipoteca

![Imagen de Encabezado](http://tinyurl.com/3rcww63x)

## Descripción del Proyecto

Este proyecto es una API de simulación de hipoteca diseñada para calcular estimaciones de préstamos hipotecarios. Puede ser utilizada por instituciones financieras o desarrolladores para proporcionar a los usuarios una forma rápida y sencilla de estimar sus pagos hipotecarios mensuales y totales.

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

3. Ejecute la aplicación:

```bash
python app.py
```

4. Acceda a la API a través de la siguiente URL local:

```bash
http://localhost:5000
```

Gracias por darme la oportunidad. Espero que el proyecto cumpla con los requisitos. Si tienen alguna pregunta, no duden en enviarme un correo electrónico.
