# 🧪 Guía de Pruebas Manuales con Swagger - Sistema KyC

**Para**: Desarrollador Backend  
**Fecha**: 29 de Diciembre, 2024  
**Versión**: 1.0  
**Herramienta**: Swagger UI (FastAPI Docs)

---

## 📑 Índice

1. [Acceso a Swagger](#acceso-swagger)
2. [Autenticación en Swagger](#autenticacion-swagger)
3. [Pruebas por Módulo](#pruebas-modulos)
4. [Checklist de Validación](#checklist-validacion)

---

## 🌐 Acceso a Swagger {#acceso-swagger}

### 1. Iniciar el servidor

```bash
cd "C:\Users\usuario\Documents\nuevos proyectos datahub\kyc"
uvicorn main:app --reload
```

### 2. Abrir Swagger UI

Abre tu navegador en:
```
http://localhost:8000/docs
```

Deberías ver la interfaz interactiva de Swagger con todos los endpoints organizados por módulos.

---

## 🔐 Autenticación en Swagger {#autenticacion-swagger}

### Paso 1: Hacer Login

1. Busca el endpoint **`POST /auth/login`**
2. Haz clic en **"Try it out"**
3. Edita el JSON del Body:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. Haz clic en **"Execute"**
5. En la respuesta, **copia el `access_token`** (sin las comillas)

### Paso 2: Autorizar en Swagger

1. Haz clic en el botón **"Authorize"** (candado verde en la parte superior derecha)
2. En el campo `HTTPBearer (http, Bearer)`, pega:
   ```
   Bearer TU_TOKEN_AQUI
   ```
   **Ejemplo**:
   ```
   Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
3. Haz clic en **"Authorize"**
4. Cierra el modal

**Ahora todos los endpoints protegidos usarán automáticamente este token.**

---

## 🧪 Pruebas por Módulo {#pruebas-modulos}

### 📋 Módulo: Inscripciones

#### Test 1: Crear Inscripción

1. Endpoint: **`POST /enrollments/`**
2. **"Try it out"**
3. Primero, obtén IDs reales:
   - Abre **`GET /students/`** → Ejecuta → Copia un `_id`
   - Abre **`GET /courses/`** → Ejecuta → Copia un `_id`
   - (Opcional) **`GET /discounts/`** → Copia un `_id`

4. Edita el Body:
   ```json
   {
     "estudiante_id": "PEGAR_ID_ESTUDIANTE",
     "curso_id": "PEGAR_ID_CURSO",
     "descuento_id": "PEGAR_ID_DESCUENTO_O_NULL"
   }
   ```

5. **Execute**

**✅ Resultado esperado**:
- Status: `201`
- Response contiene `id`, `estado: "pendiente_pago"`, `siguiente_pago`

**📝 Acción**: Copia el `id` del enrollment creado para usarlo en otros tests.

---

#### Test 2: Listar Inscripciones

1. Endpoint: **`GET /enrollments/`**
2. **"Try it out"**
3. Parámetros opcionales:
   - `page`: 1
   - `per_page`: 10
   - `estado`: (vacío o "activo")
4. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- `data`: Array de enrollments
- `meta`: Objeto con paginación

---

#### Test 3: Ver Detalle de Inscripción

1. Endpoint: **`GET /enrollments/{id}`**
2. **"Try it out"**
3. Pega el `id` del enrollment creado
4. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- Todos los campos del enrollment
- `siguiente_pago` presente

---

#### Test 4: Actualizar Estado

1. Endpoint: **`PATCH /enrollments/{id}`**
2. **"Try it out"**
3. Pega el `id`
4. Body:
   ```json
   {
     "estado": "activo"
   }
   ```
5. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- `estado` cambió a `"activo"`

---

### 💰 Módulo: Pagos

#### Test 5: Ver Siguiente Pago Sugerido ⭐

1. Endpoint: **`GET /enrollments/{id}/next-payment`**
2. **"Try it out"**
3. Pega el `id` del enrollment
4. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- Body:
  ```json
  {
    "concepto": "Matrícula",
    "numero_cuota": null,
    "monto_sugerido": 500.0
  }
  ```

**📝 Nota**: Si devuelve `null`, significa que ya pagó todo.

---

#### Test 6: Crear Pago (como Estudiante)

**IMPORTANTE**: Primero debes autenticarte como estudiante:
1. Haz logout del admin (botón "Authorize" → "Logout")
2. Login con credenciales de estudiante:
   ```json
   {
     "username": "estudiante1",
     "password": "password123"
   }
   ```
3. Autoriza con el nuevo token

Ahora:
1. Endpoint: **`POST /payments/`**
2. **"Try it out"**
3. Body:
   ```json
   {
     "inscripcion_id": "PEGAR_ID_ENROLLMENT",
     "numero_transaccion": "TRX-TEST-001",
     "comprobante_url": "https://res.cloudinary.com/demo/image/upload/sample.jpg"
   }
   ```
4. **Execute**

**✅ Resultado esperado**:
- Status: `201`
- `concepto`: "Matrícula" (calculado automáticamente)
- `estado`: `"pendiente"`

**📝 Acción**: Copia el `id` del pago creado.

---

#### Test 7: Aprobar Pago (como Admin)

**IMPORTANTE**: Vuelve a autenticarte como admin.

1. Endpoint: **`PUT /payments/{id}/aprobar`**
2. **"Try it out"**
3. Pega el `id` del pago
4. **Execute** (no necesitas Body)

**✅ Resultado esperado**:
- Status: `200`
- `estado`: `"aprobado"`

**🔍 Verificación adicional**:
- Abre **`GET /enrollments/{id}`** con el enrollment
- Verifica que `total_pagado` aumentó
- Verifica que `saldo_pendiente` disminuyó

---

#### Test 8: Rechazar Pago

**Primero crea otro pago** (repite Test 6 con `numero_transaccion: "TRX-TEST-002"`)

1. Endpoint: **`PUT /payments/{id}/rechazar`**
2. **"Try it out"**
3. Pega el `id` del nuevo pago
4. Body:
   ```json
   {
     "motivo": "El comprobante está borroso, no se puede leer el número de transacción."
   }
   ```
5. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- `estado`: `"rechazado"`
- `motivo_rechazo`: Contiene el motivo

---

#### Test 9: Intentar Crear Pago Duplicado (debe fallar)

1. Endpoint: **`POST /payments/`**
2. Usa el **mismo** `numero_transaccion` que en Test 6
3. **Execute**

**✅ Resultado esperado**:
- Status: `400`
- Mensaje: "Ya existe un pago para este concepto" o similar

---

### 📄 Módulo: Requisitos

#### Test 10: Ver Requisitos

1. Endpoint: **`GET /enrollments/{id}/requisitos`**
2. **"Try it out"**
3. Pega el `id` del enrollment
4. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- `total`: Número de requisitos
- `requisitos`: Array con cada requisito

---

#### Test 11: Subir Requisito (como Estudiante)

**IMPORTANTE**: Autentícate como estudiante.

1. Endpoint: **`PUT /enrollments/{id}/requisitos/{index}`**
2. **"Try it out"**
3. Parámetros:
   - `id`: ID del enrollment
   - `index`: 0 (primer requisito)
4. En **"file"**, haz clic en **"Choose File"** y selecciona un PDF o imagen
5. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- `estado`: `"en_proceso"`
- `url`: URL de Cloudinary

---

#### Test 12: Aprobar Requisito (como Admin)

**IMPORTANTE**: Autentícate como admin.

1. Endpoint: **`PUT /enrollments/{id}/requisitos/{index}/aprobar`**
2. **"Try it out"**
3. Parámetros:
   - `id`: ID del enrollment
   - `index`: 0
4. **Execute** (no necesitas Body)

**✅ Resultado esperado**:
- Status: `200`
- `estado`: `"aprobado"`

---

#### Test 13: Rechazar Requisito

**Primero sube otro requisito** (índice 1)

1. Endpoint: **`PUT /enrollments/{id}/requisitos/{index}/rechazar`**
2. **"Try it out"**
3. Parámetros:
   - `id`: ID del enrollment
   - `index`: 1
4. Body:
   ```json
   {
     "motivo": "Documento ilegible, por favor suba una imagen más clara"
   }
   ```
5. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- `estado`: `"rechazado"`
- `motivo_rechazo`: Contiene el motivo

---

### 📊 Módulo: Reportes

#### Test 14: Generar Reporte Excel

1. Endpoint: **`GET /payments/reportes/excel`**
2. **"Try it out"**
3. Parámetros:
   - `fecha_desde`: 2024-01-01
   - `fecha_hasta`: 2024-12-31
4. **Execute**

**✅ Resultado esperado**:
- Status: `200`
- Se descarga un archivo `.xlsx`

**🔍 Verificación manual**:
1. Abre el Excel
2. Verifica columnas: Nombre, Fecha, Moneda, Monto, Concepto, Total Cuotas, Transacción, Estado, Descripción
3. Verifica que las fechas estén en hora boliviana
4. Verifica que los filtros estén activos (flechitas ▼)

---

## ⚠️ Casos de Borde

### Test 15: Estudiante intenta crear inscripción (debe fallar)

1. Autentícate como **estudiante**
2. Endpoint: **`POST /enrollments/`**
3. **Execute** con cualquier body

**✅ Resultado esperado**:
- Status: `403`
- Mensaje: "No autorizado" o similar

---

### Test 16: Estudiante intenta aprobar pago (debe fallar)

1. Autentícate como **estudiante**
2. Endpoint: **`PUT /payments/{id}/aprobar`**
3. **Execute**

**✅ Resultado esperado**:
- Status: `403`

---

### Test 17: ID inexistente

1. Endpoint: **`GET /enrollments/{id}`**
2. Usa un ID falso: `000000000000000000000000`
3. **Execute**

**✅ Resultado esperado**:
- Status: `404`
- Mensaje: "Enrollment no encontrado"

---

## ✅ Checklist de Validación {#checklist-validacion}

Marca cada test que pase correctamente:

### Autenticación
- [ ] Login admin exitoso (token recibido)
- [ ] Login estudiante exitoso
- [ ] Login con credenciales incorrectas falla (401)
- [ ] Botón "Authorize" funciona correctamente

### Inscripciones
- [ ] Admin puede crear inscripción (201)
- [ ] Listar inscripciones con paginación (200)
- [ ] Ver detalle muestra `siguiente_pago`
- [ ] Actualizar estado funciona (200)
- [ ] Estudiante NO puede crear inscripción (403)

### Pagos
- [ ] Ver siguiente pago sugerido funciona (200)
- [ ] Estudiante puede crear pago (201)
- [ ] Admin puede aprobar pago (200)
- [ ] Admin puede rechazar pago con motivo (200)
- [ ] No se pueden crear pagos duplicados (400)
- [ ] Estudiante NO puede aprobar pagos (403)
- [ ] `total_pagado` se actualiza al aprobar
- [ ] `saldo_pendiente` se actualiza al aprobar

### Requisitos
- [ ] Ver lista de requisitos (200)
- [ ] Estudiante puede subir requisito (200)
- [ ] Admin puede aprobar requisito (200)
- [ ] Admin puede rechazar requisito (200)
- [ ] Archivo se sube correctamente

### Reportes
- [ ] Reporte Excel se genera (200)
- [ ] Columnas correctas en el Excel
- [ ] Fechas en hora boliviana
- [ ] Filtros activos en encabezados
- [ ] Estudiante NO puede generar reportes (403)

### Casos de Borde
- [ ] ID inexistente devuelve 404
- [ ] Permisos se validan correctamente (403)
- [ ] Duplicados se previenen (400)

---

## 💡 Tips para Swagger

### 1. Cambiar entre usuarios rápidamente

**Guarda los tokens**:
- Token Admin: `eyJhbGc...` (guárdalo en un notepad)
- Token Estudiante: `eyJhbGc...` (guárdalo en otro notepad)

Cuando necesites cambiar:
1. Botón "Authorize"
2. "Logout"
3. Pega el otro token
4. "Authorize"

### 2. Ver el cURL generado

Después de ejecutar un endpoint, Swagger muestra el comando `curl` equivalente. Útil para:
- Compartir con el equipo
- Automatizar tests
- Debuggear problemas

### 3. Schemas

Haz clic en **"Schemas"** (abajo en Swagger) para ver todos los modelos de datos con ejemplos.

### 4. Guardar IDs importantes

Crea un archivo `test_ids.txt` con:
```
ENROLLMENT_ID: 60d5ec49f1b2c8b1f8e4e1a1
PAYMENT_ID: 60d5ec49f1b2c8b1f8e4e1a2
STUDENT_ID: 507f1f77bcf86cd799439011
COURSE_ID: 507f191e810c19729de860ea
```

Así no tienes que buscarlos cada vez.

---

## 🎯 Flujo Completo Recomendado

Sigue este orden para probar todo el sistema de principio a fin:

1. **Login Admin** → Guardar token
2. **Crear Inscripción** → Guardar `enrollment_id`
3. **Ver Siguiente Pago** → Verificar que sugiere "Matrícula"
4. **Login Estudiante** → Guardar token
5. **Crear Pago** → Guardar `payment_id`
6. **Login Admin** nuevamente
7. **Aprobar Pago** → Verificar que `total_pagado` aumenta
8. **Ver Siguiente Pago** → Ahora debería sugerir "Cuota 1"
9. **Login Estudiante**
10. **Subir Requisito** (índice 0)
11. **Login Admin**
12. **Aprobar Requisito**
13. **Generar Reporte Excel** → Verificar que el pago aparece

---

**Elaborado por**: Equipo Backend  
**Última actualización**: 29 de Diciembre, 2024
