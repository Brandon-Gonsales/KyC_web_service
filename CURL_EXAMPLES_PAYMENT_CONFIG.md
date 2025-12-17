# Ejemplos de Comandos cURL - Payment Config API

## 🔑 Autenticación

Primero necesitas obtener un token:

```bash
# Login como Admin
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tu_admin",
    "password": "tu_password"
  }'

# Guarda el token
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 📡 Endpoints - Payment Config

### 1️⃣ Crear Configuración (ADMIN)

```bash
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_cuenta": "1234567890",
    "banco": "Banco Nacional de Bolivia",
    "titular": "Universidad Mayor de San Andrés",
    "tipo_cuenta": "Corriente",
    "qr_url": "https://res.cloudinary.com/demo/image/upload/qr_payment.png",
    "notas": "Cuenta oficial para pagos de cursos de posgrado"
  }'
```

**Response esperado (201 Created):**
```json
{
  "_id": "675f1a2b3c4d5e6f78901234",
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/demo/image/upload/qr_payment.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos de cursos de posgrado",
  "creado_por": "admin1",
  "actualizado_por": "admin1",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T18:30:00Z"
}
```

**Errores posibles:**
- `400`: Si ya existe una configuración activa
- `403`: Si no eres admin

---

### 2️⃣ Consultar Configuración (TODOS)

```bash
# Como Admin
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# Como Estudiante (con su propio token)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $STUDENT_TOKEN"
```

**Response esperado (200 OK):**
```json
{
  "_id": "675f1a2b3c4d5e6f78901234",
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/demo/image/upload/qr_payment.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos de cursos de posgrado",
  "creado_por": "admin1",
  "actualizado_por": "admin1",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T18:30:00Z"
}
```

**Errores posibles:**
- `404`: No existe configuración activa
- `401`: Token inválido o expirado

---

### 3️⃣ Actualizar Configuración (ADMIN)

#### Actualizar solo número de cuenta:
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_cuenta": "9876543210"
  }'
```

#### Actualizar QR y cuenta:
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_cuenta": "9876543210",
    "qr_url": "https://res.cloudinary.com/demo/image/upload/qr_nuevo.png"
  }'
```

#### Actualizar todos los campos:
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_cuenta": "1111222233",
    "banco": "Banco Sol",
    "titular": "Universidad UMSA",
    "tipo_cuenta": "Ahorro",
    "qr_url": "https://res.cloudinary.com/demo/qr_v2.png",
    "notas": "Nueva cuenta bancaria 2025"
  }'
```

**Response esperado (200 OK):**
```json
{
  "_id": "675f1a2b3c4d5e6f78901234",
  "numero_cuenta": "1111222233",
  "banco": "Banco Sol",
  "titular": "Universidad UMSA",
  "tipo_cuenta": "Ahorro",
  "qr_url": "https://res.cloudinary.com/demo/qr_v2.png",
  "is_active": true,
  "notas": "Nueva cuenta bancaria 2025",
  "creado_por": "admin1",
  "actualizado_por": "admin2",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T19:15:00Z"
}
```

**Errores posibles:**
- `400`: No existe configuración para actualizar
- `403`: No eres admin

---

### 4️⃣ Eliminar Configuración (ADMIN)

```bash
curl -X DELETE http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"
```

**Response esperado (200 OK):**
```json
{
  "_id": "675f1a2b3c4d5e6f78901234",
  "numero_cuenta": "1111222233",
  "banco": "Banco Sol",
  "titular": "Universidad UMSA",
  "tipo_cuenta": "Ahorro",
  "qr_url": "https://res.cloudinary.com/demo/qr_v2.png",
  "is_active": false,
  "notas": "Nueva cuenta bancaria 2025",
  "creado_por": "admin1",
  "actualizado_por": "admin2",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T19:30:00Z"
}
```

**Nota:** `is_active` cambia a `false` pero no se elimina de la base de datos.

**Errores posibles:**
- `404`: No existe configuración para eliminar
- `403`: No eres admin

---

## 🧪 Secuencia de Prueba Completa

```bash
# 1. Login como Admin
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Guardar token
export TOKEN="tu_token_aqui"

# 2. Crear configuración inicial
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_cuenta": "1234567890",
    "banco": "BNB",
    "qr_url": "https://example.com/qr.png"
  }'

# 3. Consultar configuración (debe funcionar)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Intentar crear otra (debe fallar con 400)
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_cuenta": "9999999999",
    "qr_url": "https://example.com/qr2.png"
  }'
# Esperado: Error 400 "Ya existe una configuración"

# 5. Actualizar configuración existente
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"numero_cuenta": "9999999999"}'

# 6. Verificar actualización
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# 7. Login como Estudiante
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"registro": "2024001", "password": "1234567"}'

export STUDENT_TOKEN="token_estudiante"

# 8. Estudiante consulta configuración (debe funcionar)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $STUDENT_TOKEN"

# 9. Estudiante intenta actualizar (debe fallar con 403)
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"numero_cuenta": "0000000000"}'
# Esperado: Error 403 "Forbidden"

# 10. Admin elimina configuración
curl -X DELETE http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# 11. Consultar después de eliminar (debe fallar con 404)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"
# Esperado: Error 404 "No existe configuración"
```

---

## 📝 PowerShell (Windows)

Si usas PowerShell en lugar de bash:

```powershell
# Crear configuración
$body = @{
    numero_cuenta = "1234567890"
    banco = "BNB"
    qr_url = "https://example.com/qr.png"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method POST `
  -Headers @{Authorization="Bearer $TOKEN"} `
  -ContentType "application/json" `
  -Body $body

# Consultar configuración
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method GET `
  -Headers @{Authorization="Bearer $TOKEN"}

# Actualizar configuración
$updateBody = @{
    numero_cuenta = "9999999999"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method PUT `
  -Headers @{Authorization="Bearer $TOKEN"} `
  -ContentType "application/json" `
  -Body $updateBody

# Eliminar configuración
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method DELETE `
  -Headers @{Authorization="Bearer $TOKEN"}
```

---

## 🎯 Casos de Uso Frontend

### JavaScript/Fetch

```javascript
// Obtener configuración de pagos
async function getPaymentConfig() {
  const response = await fetch('http://localhost:8000/api/v1/payment-config/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    const config = await response.json();
    
    // Mostrar QR al usuario
    document.getElementById('qr-image').src = config.qr_url;
    document.getElementById('account-number').textContent = config.numero_cuenta;
    document.getElementById('bank-name').textContent = config.banco;
    document.getElementById('account-holder').textContent = config.titular;
  } else if (response.status === 404) {
    alert('No hay configuración de pagos disponible. Contacte al administrador.');
  }
}

// Admin: Actualizar QR
async function updatePaymentQR(newQrUrl) {
  const response = await fetch('http://localhost:8000/api/v1/payment-config/', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${adminToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      qr_url: newQrUrl
    })
  });
  
  if (response.ok) {
    alert('QR actualizado exitosamente');
  }
}
```

---

## 📚 Documentación Completa

Ver archivos:
- `CONFIGURACION_PAGOS.md` - Documentación detallada
- `RESUMEN_CONFIGURACION_PAGOS.md` - Resumen ejecutivo
- `TEST_RESULTS_PAYMENT_CONFIG.md` - Resultados de pruebas

---

**Para más información consulta la documentación Swagger:**
http://localhost:8000/docs
