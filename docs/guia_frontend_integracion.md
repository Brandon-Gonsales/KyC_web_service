# 🎨 Guía de Integración Frontend - Sistema KyC

**Para**: Desarrollador Frontend  
**Fecha**: 29 de Diciembre, 2024  
**Versión**: 1.0  
**Base URL API**: `https://tu-dominio.com/api/v1`

---

## 📑 Índice

1. [Conceptos Generales](#conceptos-generales)
2. [Autenticación y Roles](#autenticacion)
3. [Módulo: Inscripciones](#modulo-inscripciones)
4. [Módulo: Pagos](#modulo-pagos)
5. [Módulo: Requisitos](#modulo-requisitos)
6. [Módulo: Reportes](#modulo-reportes)
7. [Manejo de Errores](#manejo-errores)
8. [FAQ Frontend](#faq-frontend)

---

## 🎯 Conceptos Generales {#conceptos-generales}

### ¿Qué hace este sistema?

El sistema KyC (Know Your Customer) es una plataforma de **gestión académica y financiera** para cursos. Permite:

- **Admins**: Inscribir estudiantes, aprobar pagos, revisar documentos
- **Estudiantes**: Pagar cuotas, subir requisitos, ver sus inscripciones

### Actores del Sistema

| Rol | Descripción | Interfaz Recomendada |
|-----|-------------|----------------------|
| **SuperAdmin** | Control total del sistema | Dashboard completo con módulo de usuarios |
| **Admin** | Gestiona inscripciones, pagos, requisitos | Dashboard de operaciones (sin crear otros admins) |
| **Estudiante** | Ve solo sus datos, paga, sube docs | Portal estudiante minimalista |

### Arquitectura de Comunicación

```mermaid
graph LR
    A[Frontend] -->|HTTP REST| B[API Backend]
    B -->|JWT Auth| C[MongoDB]
    B -->|Upload Files| D[Cloudinary]
    A -->|Bearer Token| B
```

**Importante**:
- Todas las peticiones (excepto `/auth/login`) requieren token JWT
- Los archivos (PDFs, imágenes) se suben a Cloudinary ANTES de enviar la URL a la API
- Las fechas vienen en formato ISO 8601, en **hora boliviana** (UTC-4)

---

## 🔐 Autenticación y Roles {#autenticacion}

### Flujo de Login

```mermaid
graph TD
    A["Usuario ingresa credenciales"] --> B["POST /auth/login"]
    B --> C{"Credenciales validas?"}
    C -->|"Si"| D["Recibir token JWT"]
    C -->|"No"| E["Error 401: Usuario/contrasena incorrectos"]
    D --> F["Guardar token en localStorage/sessionStorage"]
    F --> G["Redireccionar segun rol"]
    G -->|"Admin"| H["Dashboard Admin"]
    G -->|"Estudiante"| I["Portal Estudiante"]
```

### Endpoint de Login

**POST** `/auth/login`

**Enviar:**
```json
{
  "username": "admin123",
  "password": "MiPassword123"
}
```

**Recibir (éxito):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "username": "admin123",
    "role": "admin",
    "nombre": "Juan Pérez"
  }
}
```

**Recibir (error):**
```json
{
  "detail": "Credenciales incorrectas"
}
```

### Cómo usar el token

En TODAS las peticiones posteriores, incluir:

```
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Permisos por Rol

| Endpoint | SuperAdmin | Admin | Estudiante |
|----------|-----------|-------|------------|
| Crear Inscripción | ✅ | ✅ | ❌ |
| Ver todas las inscripciones | ✅ | ✅ | ❌ (solo las suyas) |
| Aprobar Pago | ✅ | ✅ | ❌ |
| Crear Pago | ❌ | ❌ | ✅ (solo sus enrollments) |
| Subir Requisito | ❌ | ❌ | ✅ (solo sus enrollments) |
| Aprobar Requisito | ✅ | ✅ | ❌ |
| Generar Reportes | ✅ | ✅ | ❌ |

---

## 🎓 Módulo: Inscripciones {#modulo-inscripciones}

### ¿Qué es una Inscripción (Enrollment)?

Es la **relación entre un estudiante y un curso**. Contiene:
- Información financiera (precio, descuentos, total a pagar)
- Estado académico (activo, completado, retirado)
- Requisitos (documentos que el estudiante debe subir)
- Nota final (si ya terminó)

### Flujo UI Recomendado (Admin)

```mermaid
graph TD
    A["Admin: Inscribir Estudiante"] --> B["Formulario: Seleccionar Estudiante"]
    B --> C["Seleccionar Curso"]
    C --> D["Seleccionar Descuento (dropdown de IDs)"]
    D --> E["Enviar POST /enrollments/"]
    E --> F["Mostrar resumen: Total a pagar, Cuotas"]
    F --> G["Red ireccionar a lista de inscripciones"]
```

### Endpoints Clave

#### 1. Crear Inscripción (Solo Admin)

**POST** `/enrollments/`

**Enviar:**
```json
{
  "estudiante_id": "507f1f77bcf86cd799439011",
  "curso_id": "507f191e810c19729de860ea",
  "descuento_id": "507f1f77bcf86cd799439088"
}
```

**Importante sobre descuentos:**
- Los descuentos se referencian por **ID** (`descuento_id`)
- El sistema aplicará automáticamente:
  1. Descuento del curso (si el curso tiene uno asociado)
  2. Descuento del estudiante (el que envías en `descuento_id`)
- Los descuentos se aplican en cascada (uno después del otro)

**Recibir:**
```json
{
  "id": "60d5ec49f1b2c8b1f8e4e1a1",
  "estudiante_id": "507f1f77bcf86cd799439011",
  "curso_id": "507f191e810c19729de860ea",
  "estado": "pendiente_pago",
  "total_a_pagar": 2700.0,
  "total_pagado": 0.0,
  "saldo_pendiente": 2700.0,
  "cantidad_cuotas": 12,
  "siguiente_pago": {
    "concepto": "Matrícula",
    "monto_sugerido": 500.0
  },
  "cuotas_pagadas_info": {
    "cuotas_pagadas": 0,
    "cuotas_totales": 12,
    "porcentaje": 0.0
  }
}
```

#### 2. Listar Inscripciones

**GET** `/enrollments/?page=1&per_page=10&estado=activo`

**Parámetros opcionales:**
- `page`: Número de página (default: 1)
- `per_page`: Elementos por página (max: 500)
- `q`: Búsqueda por nombre de estudiante o curso
- `estado`: Filtro por estado (pendiente_pago, activo, completado, etc.)
- `curso_id`: Filtrar por curso específico
- `estudiante_id`: Filtrar por estudiante

**Recibir:**
```json
{
  "data": [
    {
      "id": "...",
      "estudiante_id": "...",
      "estado": "activo",
      ...
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "totalItems": 36,
    "totalPages": 4,
    "hasNextPage": true,
    "hasPrevPage": false
  }
}
```

**UI Recomendada**: Tabla con paginación, filtros, y buscador.

#### 3. Ver Detalle de Inscripción

**GET** `/enrollments/{id}`

**Recibir**: Objeto completo con todos los datos financieros y académicos.

**UI Recomendada**: 
- Sección "Información del Curso"
- Sección "Progreso de Pagos" (visual: barra de progreso)
- Sección "Estado" (badge de color según estado)
- Botón "Ver Requisitos" → redirige a `/enrollments/{id}/requisitos`

#### 4. Actualizar Inscripción (Admin)

**PATCH** `/enrollments/{id}`

**Enviar** (campos opcionales):
```json
{
  "estado": "activo",
  "descuento_id": "507f1f77bcf86cd799439099",
  "nota_final": 85.5
}
```

**UI Recomendada**: Formulario con selectores para estado, selector de descuentos (dropdown con IDs), input numérico para nota.

### Estados Visuales Recomendados

| Estado | Color Badge | Icono | Descripción UI |
|--------|-------------|-------|----------------|
| `pendiente_pago` | 🟡 Amarillo | ⏳ | "Esperando pago de matrícula" |
| `activo` | 🟢 Verde | ✅ | "Curso en marcha" |
| `completado` | 🔵 Azul | 🎓 | "Pagos completados" |
| `graduado` | 🟣 Morado | 🏆 | "Curso aprobado (nota: X)" |
| `retirado` | 🔴 Rojo | ❌ | "Estudiante retirado" |
| `suspendido` | ⚫ Gris | ⏸️ | "Suspendido por admin" |

---

## 💰 Módulo: Pagos {#modulo-pagos}

### ¿Qué es un Pago?

Registro de un **comprobante de pago** subido por el estudiante. Pasa por:
1. **Pendiente**: Estudiante subió, esperando revisión
2. **Aprobado**: Admin verificó y contabilizó el dinero
3. **Rechazado**: Admin rechazó (con motivo), estudiante debe resubir

### Flujo UI Recomendado (Estudiante)

```mermaid
graph TD
    A["Estudiante: Pagar mi curso"] --> B["GET /enrollments/:id/next-payment"]
    B --> C{"Hay siguiente pago?"}
    C -->|"No"| D["Mostrar: Estas al dia!"]
    C -->|"Si"| E["Mostrar: Te toca pagar X"]
    E --> F["Formulario: Subir comprobante a Cloudinary"]
    F --> G["Input: Numero de transaccion"]
    G --> H["POST /payments/ con comprobante_url"]
    H --> I["Mostrar: Pago enviado, esperando aprobacion"]
```

### Endpoints Clave

#### 1. Ver Siguiente Pago ⭐ NUEVO

**GET** `/enrollments/{id}/next-payment`

**Recibir (si hay pago pendiente):**
```json
{
  "concepto": "Cuota 2",
  "numero_cuota": 2,
  "monto_sugerido": 500.0
}
```

**Recibir (si está al día):**
```json
null
```

**UI Recomendada**: 
- Si hay pago: Mostrar card con "Te toca pagar [concepto]: [monto] Bs"
- Si es `null`: Mostrar mensaje de felicitación + deshabilitar botón de pago

#### 2. Crear Pago (Estudiante)

**POST** `/payments/`

**Enviar:**
```json
{
  "inscripcion_id": "60d5ec49f1b2c8b1f8e4e1a1",
  "numero_transaccion": "TRX-123456",
  "comprobante_url": "https://res.cloudinary.com/tu-cloud/imagen.jpg"
}
```

**Importante**: 
- El `concepto` y `monto` se calculan automáticamente (Checklist Strategy)
- Primero sube el archivo a Cloudinary, luego envía la URL

**Recibir:**
```json
{
  "id": "...",
  "concepto": "Matrícula",
  "cantidad_pago": 500.0,
  "estado": "pendiente",
  "numero_transaccion": "TRX-123456",
  "comprobante_url": "...",
  "fecha": "2024-12-29 10:30:00"
}
```

#### 3. Listar Pagos (Admin)

**GET** `/payments/?page=1&per_page=10`

**Filtros opcionales**:
- `estado`: `pendiente`, `aprobado`, `rechazado`
- `estudiante_id`: Pagos de un estudiante
- `inscripcion_id`: Pagos de una inscripción

**UI Recomendada**: Tabla con filtros + badges de estado.

#### 4. Ver Pagos de una Inscripción

**GET** `/payments/enrollment/{enrollment_id}`

**Recibir**: Array de pagos, ordenados por fecha.

**UI Recomendada**: Timeline vertical con iconos según estado.

#### 5. Aprobar Pago (Admin)

**PUT** `/payments/{id}/aprobar`

**Enviar**: Nada (el admin se identifica por el token)

**Recibir**: Pago actualizado con `estado: "aprobado"`

**UI Recomendada**: 
- Botón verde "Aprobar" 
- Modal de confirmación: "¿Aprobar pago de [monto] Bs?"
- Tras aprobar: Actualizar badge a verde + deshabilitar botón

#### 6. Rechazar Pago (Admin)

**PUT** `/payments/{id}/rechazar`

**Enviar:**
```json
{
  "motivo": "El comprobante está borroso, no se puede leer el número de transacción."
}
```

**Recibir**: Pago con `estado: "rechazado"` y `motivo_rechazo` guardado.

**UI Recomendada**:
- Botón rojo "Rechazar"
- Modal con textarea obligatorio para el motivo
- Validación: mínimo 10 caracteres
- Tras rechazar: Badge rojo + mostrar motivo

### Estados Visuales (Pagos)

| Estado | Badge | Acciones Admin | Acciones Estudiante |
|--------|-------|----------------|---------------------|
| `pendiente` | 🟡 | Aprobar / Rechazar | Ver estado |
| `aprobado` | 🟢 | Solo ver | Ver comprobante |
| `rechazado` | 🔴 | Solo ver motivo | Ver motivo + resubir |

### Reportes Excel (Admin)

**GET** `/payments/reportes/excel?fecha_desde=2024-12-01&fecha_hasta=2024-12-31`

**Parámetros**:
- `fecha_desde`: Fecha inicio (YYYY-MM-DD)
- `fecha_hasta`: Fecha fin (YYYY-MM-DD)

**Recibir**: Archivo `.xlsx` con:
- Nombre del Estudiante
- Fecha (hora boliviana)
- Monto
- Concepto
- Estado
- Nº Transacción
- Total Cuotas
- Descripción (vacía)

**UI Recomendada**:
- Formulario con 2 date pickers
- Botón "Descargar Reporte"
- Al hacer clic: descargar automáticamente

---

## 📄 Módulo: Requisitos {#modulo-requisitos}

### ¿Qué son los Requisitos?

**Documentos** que el estudiante debe subir (ej: Carnet, CV, Título). Cada requisito tiene:
- Descripción (ej: "Cédula de Identidad frente y reverso")
- Estado (pendiente, en_proceso, aprobado, rechazado)
- URL del documento (cuando se sube)
- Motivo de rechazo (si aplica)

### Flujo UI Recomendado (Estudiante)

```mermaid
graph TD
    A["Estudiante: Mis Documentos"] --> B["GET /enrollments/:id/requisitos"]
    B --> C["Mostrar lista de requisitos"]
    C --> D{"Requisito pendiente?"}
    D -->|"Si"| E["Boton: Subir documento"]
    E --> F["Input file + validacion"]
    F --> G["Upload a Cloudinary"]
    G --> H["PUT /enrollments/:id/requisitos/:index"]
    H --> I["Estado cambia a: En Proceso"]
    D -->|"Rechazado"| J["Mostrar motivo + boton resubir"]
    D -->|"Aprobado"| K["Mostrar checkmark verde"]
```

### Endpoints Clave

#### 1. Ver Requisitos de una Inscripción

**GET** `/enrollments/{id}/requisitos`

**Recibir:**
```json
{
  "total": 3,
  "pendientes": 1,
  "en_proceso": 1,
  "aprobados": 0,
  "rechazados": 1,
  "requisitos": [
    {
      "descripcion": "Cédula de Identidad (frente y reverso)",
      "estado": "pendiente",
      "url": null,
      "motivo_rechazo": null
    },
    {
      "descripcion": "Certificado de Nacimiento",
      "estado": "en_proceso",
      "url": "https://cloudinary.com/...",
      "motivo_rechazo": null
    },
    {
      "descripcion": "CV Actualizado",
      "estado": "rechazado",
      "url": "https://cloudinary.com/old-cv.pdf",
      "motivo_rechazo": "El CV está desactualizado, debe incluir experiencia 2023-2024"
    }
  ]
}
```

**UI Recomendada**: 
- Resumen con iconos: "1 pendiente, 1 en revisión, 1 rechazado"
- Lista de cards, cada card con:
  - Título del requisito
  - Badge de estado
  - Si está rechazado: alerta roja con motivo
  - Botón "Subir" o "Ver documento"

#### 2. Subir Requisito (Estudiante)

**PUT** `/enrollments/{id}/requisitos/{index}`

**Enviar**: Archivo multipart/form-data

**Headers**:
```
Content-Type: multipart/form-data
```

**Body**:
```
file: [archivo PDF o imagen]
```

**Recibir**: Requisito actualizado con `estado: "en_proceso"`

**Validaciones Frontend**:
- Formatos permitidos: PDF, JPG, PNG, WEBP
- Tamaño máximo: 10MB (PDF), 5MB (imágenes)
- Mostrar preview antes de subir

#### 3. Aprobar Requisito (Admin)

**PUT** `/enrollments/{id}/requisitos/{index}/aprobar`

**Enviar**: Nada

**Recibir**: Requisito con `estado: "aprobado"`

**UI Recomendada**: 
- Visor de PDF/imagen
- Botón verde "Aprobar"
- Botón rojo "Rechazar" (abre modal)

#### 4. Rechazar Requisito (Admin)

**PUT** `/enrollments/{id}/requisitos/{index}/rechazar`

**Enviar:**
```json
{
  "motivo": "Documento ilegible, por favor suba una imagen más clara"
}
```

**UI Recomendada**: Modal con textarea obligatorio.

### Estados Visuales (Requisitos)

| Estado | Badge | Icono | Acción Estudiante |
|--------|-------|-------|-------------------|
| `pendiente` | ⚪ Gris | 📄 | Subir documento |
| `en_proceso` | 🟡 Amarillo | ⏳ | Esperar revisión |
| `aprobado` | 🟢 Verde | ✅ | N/A (completado) |
| `rechazado` | 🔴 Rojo | ❌ | Ver motivo + resubir |

---

## 📊 Módulo: Reportes {#modulo-reportes}

### Tipos de Reportes

| Reporte | Endpoint | Formato | Descripción |
|---------|----------|---------|-------------|
| Pagos por fecha | `/payments/reportes/excel` | Excel | Detalle de pagos en rango de fechas |

**Próximamente** (según falencias identificadas):
- Resumen financiero por curso
- Reporte de requisitos pendientes
- Dashboard analítico (CSV/JSON)

### Cómo descargar el reporte

**GET** `/payments/reportes/excel?fecha_desde=2024-01-01&fecha_hasta=2024-12-31`

**Respuesta**: Stream de archivo Excel

**Implementación Frontend**:
1. Hacer petición con `fetch` o `axios`
2. Configurar `responseType: 'blob'`
3. Crear enlace temporal y disparar descarga automática

**UI Recomendada**:
- Formulario con date pickers
- Botón "Generar Reporte"
- Mientras descarga: spinner + texto "Generando..."
- Al terminar: notificación "Reporte descargado"

---

## ⚠️ Manejo de Errores {#manejo-errores}

### Códigos de Estado HTTP

| Código | Significado | Qué hacer |
|--------|-------------|-----------|
| `200` | OK | Petición exitosa |
| `201` | Created | Recurso creado exitosamente |
| `204` | No Content | Éxito sin contenido (ej: eliminar) |
| `400` | Bad Request | Datos inválidos → mostrar mensaje específico |
| `401` | Unauthorized | Token inválido/expirado → redirigir a login |
| `403` | Forbidden | Sin permisos → mostrar "No autorizado" |
| `404` | Not Found | Recurso no existe → mostrar "No encontrado" |
| `422` | Unprocessable Entity | Validación falló → mostrar errores de campos |
| `500` | Internal Server Error | Error del servidor → "Intenta más tarde" |

### Estructura de Errores

**Formato estándar**:
```json
{
  "detail": "Inscripción no encontrada"
}
```

**Validación múltiple** (422):
```json
{
  "detail": [
    {
      "loc": ["body", "estudiante_id"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

### Recomendaciones UI

1. **401 (Token expirado)**:
   - Limpiar localStorage
   - Redirigir a `/login`
   - Mostrar: "Tu sesión expiró, inicia sesión nuevamente"

2. **403 (Sin permisos)**:
   - Mostrar modal: "No tienes permiso para esta acción"
   - No redirigir, mantener en la página actual

3. **400/422 (Datos inválidos)**:
   - Marcar campos en rojo
   - Mostrar mensaje debajo del campo
   - Ejemplo: "El descuento debe estar entre 0 y 100"

4. **500 (Error del servidor)**:
   - Mostrar toast: "Ocurrió un error, intenta más tarde"
   - Log del error (para enviar a Sentry/similar)

---

## ❓ FAQ Frontend {#faq-frontend}

### ¿Cómo sé si un usuario es Admin o Estudiante?

Al hacer login, el campo `user.role` te dirá:
- `"superadmin"` o `"admin"` → Interfaz de administración
- Si no viene `role`, es estudiante → Portal estudiante

### ¿Cómo subo archivos?

1. **Frontend**: Sube el archivo a Cloudinary usando su API
2. **Cloudinary**: Te devuelve una URL
3. **Backend**: Envía esa URL en el JSON

**No** envíes el archivo directamente a la API backend.

### ¿Qué pasa si el token expira?

El backend responde `401`. Debes:
1. Capturar el error global (interceptor de Axios)
2. Limpiar el token guardado
3. Redirigir a `/login`

### ¿Cómo pagino correctamente?

Los endpoints con paginación devuelven:
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "totalPages": 10,
    "hasNextPage": true,
    "hasPrevPage": false
  }
}
```

Usa `meta.hasNextPage` para habilitar/deshabilitar botón "Siguiente".

### ¿Cómo muestro el progreso de pagos?

El endpoint `/enrollments/{id}` devuelve:
```json
{
  "cuotas_pagadas_info": {
    "cuotas_pagadas": 3,
    "cuotas_totales": 12,
    "porcentaje": 25.0
  }
}
```

Renderiza una barra de progreso con `porcentaje` o un texto "3/12 cuotas pagadas".

### ¿Qué hacer si un pago fue rechazado?

1. Mostrar el `motivo_rechazo` en rojo
2. Permitir crear un nuevo pago (el backend automáticamente sugerirá el mismo concepto)
3. El pago rechazado queda como histórico (no se borra)

### ¿Cómo valido formularios antes de enviar?

**Recomendaciones**:
- Descuentos: 0-100%
- Montos: > 0
- Fechas: formato YYYY-MM-DD
- Archivos: extensiones permitidas + tamaño máximo
- Campos de texto: trim() para evitar espacios

### ¿Las fechas están en UTC o hora local?

Las fechas que vienen de la API están en **hora boliviana** (UTC-4).

**Ejemplo**: 
- API devuelve: `"2024-12-29 10:30:00"`
- Esto ya es hora Bolivia
- **No** necesitas convertir, muéstralo directamente

### ¿Qué endpoints requieren paginación?

- `/enrollments/`
- `/payments/`
- Cualquier lista que pueda crecer mucho

Usa siempre `?page=1&per_page=10` o similar.

---

## 🎨 Recomendaciones de UX

### Dashboard Admin

**Secciones recomendadas**:
1. **Resumen**: Cards con totales (inscripciones activas, pagos pendientes, requisitos por revisar)
2. **Acciones rápidas**: Botones "Inscribir estudiante", "Revisar pagos", "Ver reportes"
3. **Listas**: Tablas con paginación y filtros

### Portal Estudiante

**Secciones recomendadas**:
1. **Mis cursos**: Cards con cada inscripción + estado visual
2. **Pagos**: Timeline de pagos (aprobados, pendientes, rechazados)
3. **Documentos**: Checklist de requisitos con progreso visual
4. **Botón destacado**: "Pagar mi curso" (si hay siguiente pago)

### Colores Recomendados

| Elemento | Color | Hex |
|----------|-------|-----|
| Éxito (aprobado, activo) | Verde | `#10B981` |
| Advertencia (pendiente) | Amarillo | `#F59E0B` |
| Error (rechazado, suspendido) | Rojo | `#EF4444` |
| Info (completado) | Azul | `#3B82F6` |
| Neutral (retirado) | Gris | `#6B7280` |

### Íconos Sugeridos

- ✅ Aprobado
- ⏳ Pendiente
- ❌ Rechazado
- 📄 Documento
- 💰 Pago
- 🎓 Curso
- 📊 Reporte
- 🔔 Notificación

---

## 📞 Contacto con Backend

Si encuentras errores o necesitas un endpoint nuevo:
1. Documenta el caso de uso
2. Especifica qué datos necesitas
3. Propón el endpoint ideal

**Ejemplo**:
> "Necesito filtrar pagos por rango de fechas y estado al mismo tiempo.  
> Propongo: `GET /payments/?fecha_desde=X&fecha_hasta=Y&estado=aprobado`"

---

**Elaborado por**: Equipo Backend  
**Próxima revisión**: Al agregar nuevos módulos
