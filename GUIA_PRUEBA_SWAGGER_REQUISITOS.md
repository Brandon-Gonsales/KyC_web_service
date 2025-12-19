# 🧪 GUÍA DE PRUEBA: Sistema de Requisitos Dinámicos en Swagger

## 📋 OBJETIVO

Probar el flujo completo del sistema de requisitos dinámicos desde Swagger UI:
1. Crear un curso con requisitos
2. Inscribir un estudiante
3. Ver requisitos del enrollment
4. Subir documentos como estudiante
5. Aprobar/Rechazar como admin

---

## 🌐 ACCEDER A SWAGGER

1. Abre tu navegador
2. Ve a: **http://localhost:8000/docs**
3. Verás la documentación interactiva de la API

---

## 🔐 PASO 1: AUTENTICACIÓN

### 1.1 Login como Admin

**Endpoint:** `POST /api/v1/auth/login`

1. Click en el endpoint
2. Click en "Try it out"
3. En el body, pon:
```json
{
  "registro": "TU_ADMIN_REGISTRO",
  "password": "TU_PASSWORD"
}
```
4. Click "Execute"
5. **Copia el `access_token`** de la respuesta

### 1.2 Autorizar en Swagger

1. Click en el botón **"Authorize"** (arriba a la derecha, icono de candado)
2. En el campo, escribe: `Bearer TU_TOKEN_AQUI`
3. Click "Authorize"
4. Click "Close"

✅ **Ahora estás autenticado como Admin**

---

## 📚 PASO 2: CREAR UN CURSO CON REQUISITOS

**Endpoint:** `POST /api/v1/courses/`

### Datos de Ejemplo:

```json
{
  "codigo": "DIPL-IA-2024",
  "nombre_programa": "Diplomado en Inteligencia Artificial",
  "tipo_curso": "diplomado",
  "modalidad": "híbrido",
  "costo_total_interno": 3000,
  "matricula_interno": 500,
  "costo_total_externo": 5000,
  "matricula_externo": 800,
  "cantidad_cuotas": 12,
  "descuento_curso": 0,
  "observacion": "Incluye certificación internacional",
  "fecha_inicio": "2025-03-01T00:00:00",
  "fecha_fin": "2025-08-31T00:00:00",
  "activo": True,
  "requisitos": [
    {
      "descripcion": "CV actualizado (máximo 2 años de antigüedad)"
    },
    {
      "descripcion": "Fotocopia de carnet de identidad (ambas caras)"
    },
    {
      "descripcion": "Título profesional o certificado de egreso"
    },
    {
      "descripcion": "Certificado de afiliación profesional (si aplica)"
    }
  ]
}
```

### Resultado Esperado:

```json
{
  "_id": "675f...",
  "codigo": "DIPL-IA-2024",
  "nombre_programa": "Diplomado en Inteligencia Artificial",
  "requisitos": [
    {"descripcion": "CV actualizado..."},
    {"descripcion": "Fotocopia de carnet..."},
    {"descripcion": "Título profesional..."},
    {"descripcion": "Certificado de afiliación..."}
  ],
  ...
}
```

✅ **Copia el `_id` del curso creado**

---

## 👥 PASO 3: VERIFICAR ESTUDIANTES

**Endpoint:** `GET /api/v1/students/`

1. Click en el endpoint
2. Click "Try it out"
3. Click "Execute"
4. Busca un estudiante de la lista

✅ **Copia el `_id` de un estudiante**

---

## 📝 PASO 4: CREAR ENROLLMENT

**Endpoint:** `POST /api/v1/enrollments/`

### Datos:

```json
{
  "estudiante_id": "STUDENT_ID_AQUI",
  "curso_id": "COURSE_ID_AQUI",
  "descuento_personalizado": 0
}
```

### Resultado Esperado:

```json
{
  "_id": "675f...",
  "estudiante_id": "...",
  "curso_id": "...",
  "estado": "pendiente_pago",
  "requisitos": [
    {
      "descripcion": "CV actualizado (máximo 2 años de antigüedad)",
      "estado": "pendiente",
      "url": null,
      "motivo_rechazo": null,
      "revisado_por": null,
      "fecha_subida": null
    },
    {
      "descripcion": "Fotocopia de carnet de identidad (ambas caras)",
      "estado": "pendiente",
      "url": null
    },
    {
      "descripcion": "Título profesional o certificado de egreso",
      "estado": "pendiente",
      "url": null
    },
    {
      "descripcion": "Certificado de afiliación profesional (si aplica)",
      "estado": "pendiente",
      "url": null
    }
  ],
  ...
}
```

✅ **Observa que los requisitos se copiaron automáticamente del curso**
✅ **Todos están en estado `pendiente`**
✅ **Copia el `_id` del enrollment**

---

## 📊 PASO 5: VER REQUISITOS CON ESTADÍSTICAS

**Endpoint:** `GET /api/v1/enrollments/{id}/requisitos`

1. Click en el endpoint
2. Click "Try it out"
3. En `id`, pon el enrollment ID
4. Click "Execute"

### Resultado Esperado:

```json
{
  "total": 4,
  "pendientes": 4,
  "en_proceso": 0,
  "aprobados": 0,
  "rechazados": 0,
  "requisitos": [
    {
      "descripcion": "CV actualizado (máximo 2 años de antigüedad)",
      "estado": "pendiente",
      "url": null,
      "motivo_rechazo": null,
      "revisado_por": null,
      "fecha_subida": null
    },
    // ... otros 3 requisitos
  ]
}
```

✅ **Muestra estadísticas claras del progreso**

---

## 🔄 PASO 6: CAMBIAR A ESTUDIANTE

### 6.1 Logout del Admin

1. Click en "Authorize"
2. Click "Logout"

### 6.2 Login como Estudiante

**Endpoint:** `POST /api/v1/auth/login`

```json
{
  "registro": "REGISTRO_DEL_ESTUDIANTE",
  "password": "PASSWORD_ESTUDIANTE"
}
```

✅ Copia el token y autoriza de nuevo

---

## 📤 PASO 7: SUBIR REQUISITO (COMO ESTUDIANTE)

**Endpoint:** `PUT /api/v1/enrollments/{id}/requisitos/{index}`

### Parámetros:
- **id**: ID del enrollment
- **index**: Índice del requisito (0, 1, 2, o 3)
- **file**: Archivo PDF o imagen

### Proceso en Swagger:

1. Click en el endpoint
2. Click "Try it out"
3. En `id`: pon el enrollment ID
4. En `index`: pon `0` (para el primer requisito - CV)
5. En `file`: Click "Choose File" y selecciona un PDF o imagen
6. Click "Execute"

### Resultado Esperado:

```json
{
  "descripcion": "CV actualizado (máximo 2 años de antigüedad)",
  "estado": "en_proceso",
  "url": "https://res.cloudinary.com/.../req_0_CV_actualizado.pdf",
  "motivo_rechazo": null,
  "revisado_por": null,
  "fecha_subida": "2024-12-18T20:30:00Z"
}
```

✅ **Estado cambió a `en_proceso`**
✅ **URL de Cloudinary generada**
✅ **Fecha de subida registrada**

### Subir Más Requisitos:

Repite con diferentes índices:
- `index = 1` para "Fotocopia de carnet"
- `index = 2` para "Título profesional"
- `index = 3` para "Certificado de afiliación"

---

## 👁️ PASO 8: VERIFICAR PROGRESO

**Endpoint:** `GET /api/v1/enrollments/{id}/requisitos`

```json
{
  "total": 4,
  "pendientes": 1,
  "en_proceso": 3,
  "aprobados": 0,
  "rechazados": 0,
  "requisitos": [...]
}
```

✅ **Las estadísticas se actualizan automáticamente**

---

## 🔄 PASO 9: VOLVER A ADMIN

1. Logout del estudiante
2. Login con tu admin
3. Autoriza de nuevo

---

## ✅ PASO 10: APROBAR REQUISITO

**Endpoint:** `PUT /api/v1/enrollments/{id}/requisitos/{index}/aprobar`

1. Click en el endpoint
2. Click "Try it out"
3. `id`: enrollment ID
4. `index`: `0` (aprobar el CV)
5. Click "Execute"

### Resultado Esperado:

```json
{
  "descripcion": "CV actualizado (máximo 2 años de antigüedad)",
  "estado": "aprobado",
  "url": "https://res.cloudinary.com/.../req_0_CV_actualizado.pdf",
  "motivo_rechazo": null,
  "revisado_por": "admin1",
  "fecha_subida": "2024-12-18T20:30:00Z"
}
```

✅ **Estado cambió a `aprobado`**
✅ **`revisado_por` tiene el username del admin**

---

## ❌ PASO 11: RECHAZAR REQUISITO

**Endpoint:** `PUT /api/v1/enrollments/{id}/requisitos/{index}/rechazar`

1. Click en el endpoint
2. Click "Try it out"
3. `id`: enrollment ID
4. `index`: `1` (rechazar el carnet)
5. En el body:

```json
{
  "motivo": "La fotocopia está muy borrosa. Por favor, escanee con mejor resolución o tome foto con buena iluminación."
}
```

6. Click "Execute"

### Resultado Esperado:

```json
{
  "descripcion": "Fotocopia de carnet de identidad (ambas caras)",
  "estado": "rechazado",
  "url": "https://res.cloudinary.com/.../req_1_carnet.jpg",
  "motivo_rechazo": "La fotocopia está muy borrosa. Por favor, escanee con mejor resolución...",
  "revisado_por": "admin1",
  "fecha_subida": "2024-12-18T20:31:00Z"
}
```

✅ **Estado cambió a `rechazado`**
✅ **`motivo_rechazo` guardado**
✅ **`revisado_por` registrado**

---

## 🔄 PASO 12: RESUBIR REQUISITO RECHAZADO (ESTUDIANTE)

1. Logout del admin
2. Login como estudiante
3. Usar: `PUT /api/v1/enrollments/{id}/requisitos/1`
4. Subir un archivo nuevo

### Resultado:

```json
{
  "descripcion": "Fotocopia de carnet de identidad (ambas caras)",
  "estado": "en_proceso",
  "url": "https://res.cloudinary.com/.../req_1_carnet.jpg",
  "motivo_rechazo": null,
  "revisado_por": null,
  "fecha_subida": "2024-12-18T20:45:00Z"
}
```

✅ **Estado vuelve a `en_proceso`**
✅ **`motivo_rechazo` se limpia**
✅ **Nueva `fecha_subida`**

---

## 📊 PASO 13: ESTADO FINAL

**Endpoint:** `GET /api/v1/enrollments/{id}/requisitos`

```json
{
  "total": 4,
  "pendientes": 0,
  "en_proceso": 2,
  "aprobados": 1,
  "rechazados": 0,
  "requisitos": [
    {
      "descripcion": "CV actualizado",
      "estado": "aprobado",
      "revisado_por": "admin1"
    },
    {
      "descripcion": "Fotocopia de carnet",
      "estado": "en_proceso",
      "motivo_rechazo": null
    },
    {
      "descripcion": "Título profesional",
      "estado": "en_proceso"
    },
    {
      "descripcion": "Certificado de afiliación",
      "estado": "pendiente"
    }
  ]
}
```

---

## ✅ CHECKLIST DE FUNCIONALIDADES

Durante la prueba, verifica que:

### ✅ Creación de Curso:
- [ ] Se pueden agregar múltiples requisitos
- [ ] Los requisitos se guardan correctamente

### ✅ Creación de Enrollment:
- [ ] Los requisitos se copian automáticamente del curso
- [ ] Todos inician en estado `pendiente`
- [ ] Todos tienen `url: null`

### ✅ Listado de Requisitos:
- [ ] Muestra estadísticas correctas
- [ ] Muestra todos los requisitos
- [ ] Admin puede ver cualquier enrollment
- [ ] Estudiante solo ve sus enrollments

### ✅ Subida de Requisito:
- [ ] Acepta PDF
- [ ] Acepta imágenes (JPG, PNG, WEBP)
- [ ] Rechaza otros formatos
- [ ] Cambia estado a `en_proceso`
- [ ] Genera URL de Cloudinary
- [ ] Registra `fecha_subida`
- [ ] Estudiante solo puede subir a sus enrollments

### ✅ Aprobación de Requisito:
- [ ] Solo admin puede aprobar
- [ ] Cambia estado a `aprobado`
- [ ] Registra `revisado_por`
- [ ] Limpia `motivo_rechazo` si existía

### ✅ Rechazo de Requisito:
- [ ] Solo admin puede rechazar
- [ ] Cambia estado a `rechazado`
- [ ] Guarda `motivo_rechazo`
- [ ] Registra `revisado_por`

### ✅ Resubida:
- [ ] Estudiante puede resubir requisito rechazado
- [ ] Estado vuelve a `en_proceso`
- [ ] `motivo_rechazo` se limpia
- [ ] Nueva `fecha_subida`

---

## 🔍 VALIDACIONES A PROBAR

### ❌ Errores Esperados:

1. **Subir a enrollment de otro estudiante:**
   ```
   403: "No es tu enrollment"
   ```

2. **Aprobar sin documento subido:**
   ```
   400: "No se puede aprobar sin documento"
   ```

3. **Índice fuera de rango:**
   ```
   400: "Índice 10 fuera de rango. Este enrollment tiene 4 requisitos"
   ```

4. **Formato de archivo no permitido:**
   ```
   400: "Formato no permitido: application/zip"
   ```

5. **Aprobar requisito pendiente:**
   ```
   400: "No se puede aprobar en estado pendiente"
   ```

---

## 🎨 INTERFAZ DE USUARIO (FUTURO)

Así se vería en el frontend:

### Vista del Estudiante:
```
📋 Mis Requisitos
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Progreso: 1/4 aprobados (25%)

[✅] CV actualizado
     Estado: APROBADO
     Revisado por: admin1

[🔄] Fotocopia de carnet
     Estado: EN REVISIÓN
     [Subir nuevo archivo]

[📤] Título profesional
     Estado: EN REVISIÓN

[⏳] Certificado de afiliación
     Estado: PENDIENTE
     [📎 Subir documento]
```

### Vista del Admin:
```
📋 Requisitos del Estudiante
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Juan Pérez - Diplomado en IA

[🔄] CV actualizado
     [📄 Ver documento]
     [✅ Aprobar] [❌ Rechazar]

[🔄] Fotocopia de carnet
     [📄 Ver documento]
     [✅ Aprobar] [❌ Rechazar]
```

---

## 🚀 FLUJO COMPLETO RESUMIDO

```
1. ADMIN → Crea curso con requisitos
          ↓
2. ADMIN → Inscribe estudiante
          ↓
    Sistema copia requisitos automáticamente (PENDIENTE)
          ↓
3. ESTUDIANTE → Sube CV
          ↓
    Estado: PENDIENTE → EN_PROCESO
          ↓
4. ADMIN → Revisa y aprueba CV
          ↓
    Estado: EN_PROCESO → APROBADO
          ↓
5. ESTUDIANTE → Sube carnet
          ↓
6. ADMIN → Rechaza carnet (foto borrosa)
          ↓
    Estado: EN_PROCESO → RECHAZADO
          ↓
7. ESTUDIANTE → Resubmite carnet (mejor foto)
          ↓
    Estado: RECHAZADO → EN_PROCESO
          ↓
8. ADMIN → Aprueba carnet
          ↓
    Estado: EN_PROCESO → APROBADO
          ↓
✅ COMPLETADO
```

---

## 📝 NOTAS IMPORTANTES

1. **Cloudinary** debe estar configurado correctamente en `.env`
2. **Tokens** expiran (configurado en ACCESS_TOKEN_EXPIRE_MINUTES)
3. **Archivos** se organizan en Cloudinary: `enrollments/{enrollment_id}/requisitos/req_{index}_{descripcion}`
4. **Índices** empiezan en 0 (primer requisito = 0)
5. **Estados** son inmutables via API (solo cambian con los endpoints específicos)

---

¡Listo para probar! 🎉

**URL Swagger:** http://localhost:8000/docs
