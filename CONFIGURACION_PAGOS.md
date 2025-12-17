# Sistema de Configuración de Pagos

## 📌 Descripción General

Este módulo permite gestionar la **configuración global de pagos** del sistema, incluyendo:
- **QR de pago** (imagen)
- **Número de cuenta bancaria**
- **Información adicional** (banco, titular, tipo de cuenta)

**IMPORTANTE**: Solo puede existir **UNA configuración activa** a la vez (patrón singleton).

---

## 🎯 Casos de Uso

### 1. **Estudiantes**
Los estudiantes necesitan consultar esta información para:
- Ver el QR al momento de realizar un pago
- Conocer el número de cuenta donde depositar
- Obtener datos del banco y titular para transferencias

### 2. **Administradores**
Los administradores pueden:
- Crear la configuración inicial del sistema
- Actualizar la cuenta bancaria cuando cambie
- Actualizar el QR si cambia el sistema de pagos
- Ver quién creó/modificó la configuración y cuándo

---

## 🔐 Permisos

| Operación | Admin | Student |
|-----------|-------|---------|
| **Crear configuración** | ✅ | ❌ |
| **Consultar configuración** | ✅ | ✅ |
| **Actualizar configuración** | ✅ | ❌ |
| **Eliminar configuración** | ✅ | ❌ |

---

## 📡 Endpoints Disponibles

### Base URL
```
/api/v1/payment-config
```

---

### 1. **Crear Configuración** (Admin)

**`POST /api/v1/payment-config/`**

**Requiere**: ADMIN o SUPERADMIN

**Body:**
```json
{
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/.../qr_pago.png",
  "notas": "Cuenta oficial para pagos de cursos de posgrado"
}
```

**Response (201):**
```json
{
  "_id": "507f1f77bcf86cd799439099",
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/.../qr_pago.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos",
  "creado_por": "admin1",
  "actualizado_por": "admin1",
  "created_at": "2024-12-17T10:00:00",
  "updated_at": "2024-12-17T10:00:00"
}
```

**Errores:**
- `400 Bad Request`: Si ya existe una configuración activa
- `403 Forbidden`: Si no es admin

---

### 2. **Consultar Configuración** (Todos)

**`GET /api/v1/payment-config/`**

**Requiere**: Usuario autenticado (Admin o Student)

**Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439099",
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/.../qr_pago.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos",
  "creado_por": "admin1",
  "actualizado_por": "admin2",
  "created_at": "2024-12-17T10:00:00",
  "updated_at": "2024-12-17T14:00:00"
}
```

**Errores:**
- `404 Not Found`: Si no existe configuración activa
- `401 Unauthorized`: Si no está autenticado

---

### 3. **Actualizar Configuración** (Admin)

**`PUT /api/v1/payment-config/`**

**Requiere**: ADMIN o SUPERADMIN

**Body (todos los campos son opcionales):**
```json
{
  "numero_cuenta": "9876543210",
  "qr_url": "https://res.cloudinary.com/.../qr_nuevo.png"
}
```

**Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439099",
  "numero_cuenta": "9876543210",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/.../qr_nuevo.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos",
  "creado_por": "admin1",
  "actualizado_por": "admin2",
  "created_at": "2024-12-17T10:00:00",
  "updated_at": "2024-12-17T16:00:00"
}
```

**Errores:**
- `400 Bad Request`: Si no existe configuración para actualizar
- `403 Forbidden`: Si no es admin

---

### 4. **Eliminar Configuración** (Admin)

**`DELETE /api/v1/payment-config/`**

**Requiere**: ADMIN o SUPERADMIN

**Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439099",
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/.../qr_pago.png",
  "is_active": false,
  "notas": "Cuenta oficial para pagos",
  "creado_por": "admin1",
  "actualizado_por": "admin1",
  "created_at": "2024-12-17T10:00:00",
  "updated_at": "2024-12-17T18:00:00"
}
```

**IMPORTANTE**: Esta operación NO elimina permanentemente la configuración, solo la marca como `is_active: false`.

**Errores:**
- `404 Not Found`: Si no existe configuración para eliminar
- `403 Forbidden`: Si no es admin

---

## 🔄 Flujo Típico de Uso

### Configuración Inicial (Admin)

```
1. Admin crea la configuración inicial
   POST /api/v1/payment-config/
   {
     "numero_cuenta": "1234567890",
     "banco": "BNB",
     "qr_url": "https://..."
   }

2. Sistema guarda la configuración (is_active = true)
```

### Consulta de Información (Estudiante)

```
1. Estudiante quiere realizar un pago
   
2. Frontend consulta la configuración
   GET /api/v1/payment-config/
   
3. Sistema retorna QR y número de cuenta
   
4. Frontend muestra al estudiante:
   - Imagen del QR
   - Número de cuenta: 1234567890
   - Banco: BNB
   - Titular: UMSA
   
5. Estudiante realiza el pago y sube comprobante
   POST /api/v1/payments/
```

### Actualización de Cuenta (Admin)

```
1. Admin necesita cambiar el número de cuenta
   
2. Admin actualiza la configuración
   PUT /api/v1/payment-config/
   {
     "numero_cuenta": "9876543210",
     "qr_url": "https://.../nuevo_qr.png"
   }

3. Sistema actualiza la configuración
   (actualizado_por = admin_username)
   
4. Desde ese momento, todos los usuarios verán
   la nueva información al consultar
```

---

## ⚠️ Consideraciones Importantes

### 1. **Patrón Singleton**
- Solo puede existir **UNA** configuración activa
- Si intentas crear otra, te dará error 400
- Debes actualizar la existente en lugar de crear una nueva

### 2. **Eliminación Soft**
- `DELETE` no borra permanentemente la configuración
- Solo la marca como `is_active: false`
- Esto permite mantener historial y auditoría

### 3. **Impacto en el Sistema**
- Sin configuración activa, los estudiantes NO podrán ver el QR ni cuenta
- Asegúrate de que siempre exista una configuración activa
- Actualiza en lugar de eliminar cuando sea posible

### 4. **Cloudinary para QR**
- El `qr_url` debe ser una URL pública de Cloudinary
- Sube primero la imagen del QR a Cloudinary
- Luego usa la URL en la configuración

### 5. **Auditoría**
- El sistema registra quién creó y actualizó la configuración
- Cada cambio actualiza el campo `actualizado_por`
- Las fechas se actualizan automáticamente

---

## 🛠️ Estructura de Archivos

```
kyc/
├── models/
│   └── payment_config.py      # Modelo de configuración
├── schemas/
│   └── payment_config.py      # Schemas (Create, Update, Response)
├── services/
│   └── payment_config_service.py  # Lógica de negocio
└── api/
    └── payment_config.py      # Endpoints de la API
```

---

## 📝 Ejemplo de Integración Frontend

### Mostrar QR al Estudiante

```javascript
// 1. Obtener configuración de pagos
const response = await fetch('/api/v1/payment-config/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const config = await response.json();

// 2. Mostrar al usuario
document.getElementById('qr').src = config.qr_url;
document.getElementById('cuenta').textContent = config.numero_cuenta;
document.getElementById('banco').textContent = config.banco;
document.getElementById('titular').textContent = config.titular;
```

### Panel de Admin para Actualizar

```javascript
// Actualizar QR y cuenta
const response = await fetch('/api/v1/payment-config/', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${adminToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    numero_cuenta: newAccountNumber,
    qr_url: newQrUrl
  })
});

const updated = await response.json();
console.log('Configuración actualizada:', updated);
```

---

## ✅ Resumen

| Característica | Detalle |
|----------------|---------|
| **Patrón** | Singleton (una sola configuración activa) |
| **Acceso Lectura** | Cualquier usuario autenticado |
| **Acceso Escritura** | Solo ADMIN/SUPERADMIN |
| **Eliminación** | Soft delete (marca como inactivo) |
| **Auditoría** | Registra quién crea/actualiza y cuándo |
| **Campos Principales** | `numero_cuenta`, `qr_url`, `banco`, `titular` |

---

**Documento creado**: 17 de Diciembre de 2024  
**Sistema**: KyC Payment System API  
**Versión**: 1.0
