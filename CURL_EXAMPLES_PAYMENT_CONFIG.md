# Ejemplos de Comandos cURL - Payment Config API (CON UPLOAD DE IMAGEN)

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

## 📡 Endpoints - Payment Config (multipart/form-data)

### 1️⃣ Crear Configuración con Upload de QR (ADMIN)

```bash
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/ruta/a/tu/qr_image.png" \
  -F "numero_cuenta=1234567890" \
  -F "banco=Banco Nacional de Bolivia" \
  -F "titular=Universidad Mayor de San Andrés" \
  -F "tipo_cuenta=Corriente" \
  -F "notas=Cuenta oficial para pagos de cursos de posgrado"
```

**Explicación:**
- `-F "file=@/ruta/a/tu/qr_image.png"` - Sube la imagen del QR desde tu computadora
- El servidor automáticamente sube la imagen a Cloudinary
- Guarda la URL generada en la base de datos

**Response esperado (201 Created):**
```json
{
  "_id": "675f1a2b3c4d5e6f78901234",
  "numero_cuenta": "1234567890",
  "banco": "Banco Nacional de Bolivia",
  "titular": "Universidad Mayor de San Andrés",
  "tipo_cuenta": "Corriente",
  "qr_url": "https://res.cloudinary.com/tu-cloud/image/upload/payment_config/qr_payment.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos de cursos de posgrado",
  "creado_por": "admin1",
  "actualizado_por": "admin1",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T18:30:00Z"
}
```

**Formatos de imagen soportados:**
- JPG/JPEG
- PNG
- WEBP
- Tamaño máximo: 5MB

**Errores posibles:**
- `400`: Si ya existe una configuración activa
- `400`: Si el archivo no es una imagen válida
- `400`: Si la imagen es muy grande (>5MB)
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
  "qr_url": "https://res.cloudinary.com/tu-cloud/image/upload/payment_config/qr_payment.png",
  "is_active": true,
  "notas": "Cuenta oficial para pagos de cursos de posgrado",
  "creado_por": "admin1",
  "actualizado_por": "admin1",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T18:30:00Z"
}
```

**Frontend puede usar `qr_url` directamente:**
```html
<img src="https://res.cloudinary.com/.../qr_payment.png" alt="QR de Pago" />
```

---

### 3️⃣ Actualizar Configuración (ADMIN)

#### a) Actualizar solo número de cuenta (sin cambiar QR):
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "numero_cuenta=9876543210"
```

#### b) Actualizar solo el QR (nueva imagen):
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/ruta/a/nuevo_qr.png"
```

#### c) Actualizar QR y número de cuenta:
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/ruta/a/nuevo_qr.png" \
  -F "numero_cuenta=9876543210"
```

#### d) Actualizar todos los campos:
```bash
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/ruta/a/qr_v2.png" \
  -F "numero_cuenta=1111222233" \
  -F "banco=Banco Sol" \
  -F "titular=Universidad UMSA" \
  -F "tipo_cuenta=Ahorro" \
  -F "notas=Nueva cuenta bancaria 2025"
```

**Response esperado (200 OK):**
```json
{
  "_id": "675f1a2b3c4d5e6f78901234",
  "numero_cuenta": "1111222233",
  "banco": "Banco Sol",
  "titular": "Universidad UMSA",
  "tipo_cuenta": "Ahorro",
  "qr_url": "https://res.cloudinary.com/tu-cloud/image/upload/payment_config/qr_payment.png",
  "is_active": true,
  "notas": "Nueva cuenta bancaria 2025",
  "creado_por": "admin1",
  "actualizado_por": "admin2",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T19:15:00Z"
}
```

**Nota**: El QR se reemplaza automáticamente en Cloudinary. La URL se mantiene igual pero muestra la nueva imagen.

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
  "qr_url": "https://res.cloudinary.com/tu-cloud/image/upload/payment_config/qr_payment.png",
  "is_active": false,
  "notas": "Nueva cuenta bancaria 2025",
  "creado_por": "admin1",
  "actualizado_por": "admin2",
  "created_at": "2024-12-17T18:30:00Z",
  "updated_at": "2024-12-17T19:30:00Z"
}
```

**Nota:** `is_active` cambia a `false` pero el QR permanece en Cloudinary.

---

## 🧪 Secuencia de Prueba Completa

```bash
# 1. Login como Admin
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Guardar token
export TOKEN="tu_token_aqui"

# 2. Crear configuración con imagen QR
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./qr_bnb.png" \
  -F "numero_cuenta=1234567890" \
  -F "banco=BNB" \
  -F "titular=UMSA"

# 3. Consultar configuración (debe funcionar)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Intentar crear otra (debe fallar con 400)
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./otro_qr.png" \
  -F "numero_cuenta=9999999999"
# Esperado: Error 400 "Ya existe una configuración"

# 5. Actualizar solo número de cuenta
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "numero_cuenta=9999999999"

# 6. Actualizar QR con nueva imagen
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@./nuevo_qr.png"

# 7. Verificar actualización
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# 8. Login como Estudiante
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"registro": "2024001", "password": "1234567"}'

export STUDENT_TOKEN="token_estudiante"

# 9. Estudiante consulta configuración (debe funcionar)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $STUDENT_TOKEN"

# 10. Estudiante intenta actualizar (debe fallar con 403)
curl -X PUT http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -F "numero_cuenta=0000000000"
# Esperado: Error 403 "Forbidden"

# 11. Admin elimina configuración
curl -X DELETE http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"

# 12. Consultar después de eliminar (debe fallar con 404)
curl -X GET http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN"
# Esperado: Error 404 "No existe configuración"
```

---

## 📝 PowerShell (Windows)

Si usas PowerShell en lugar de bash:

```powershell
# Crear configuración con imagen
$headers = @{
    Authorization = "Bearer $TOKEN"
}

$form = @{
    file = Get-Item -Path "C:\ruta\a\qr_image.png"
    numero_cuenta = "1234567890"
    banco = "BNB"
    titular = "UMSA"
    tipo_cuenta = "Corriente"
    notas = "Cuenta oficial"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method POST `
  -Headers $headers `
  -Form $form

# Consultar configuración
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method GET `
  -Headers @{Authorization="Bearer $TOKEN"}

# Actualizar solo número de cuenta
$updateForm = @{
    numero_cuenta = "9999999999"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method PUT `
  -Headers $headers `
  -Form $updateForm

# Actualizar QR
$updateWithFile = @{
    file = Get-Item -Path "C:\ruta\a\nuevo_qr.png"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method PUT `
  -Headers $headers `
  -Form $updateWithFile

# Eliminar configuración
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/payment-config/" `
  -Method DELETE `
  -Headers @{Authorization="Bearer $TOKEN"}
```

---

## 🎯 Casos de Uso Frontend

### JavaScript/Fetch con FormData

```javascript
// Crear configuración con imagen QR
async function createPaymentConfig(imageFile, data) {
  const formData = new FormData();
  formData.append('file', imageFile); // File object del input
  formData.append('numero_cuenta', data.numero_cuenta);
  formData.append('banco', data.banco);
  formData.append('titular', data.titular);
  formData.append('tipo_cuenta', data.tipo_cuenta);
  formData.append('notas', data.notas);
  
  const response = await fetch('http://localhost:8000/api/v1/payment-config/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${adminToken}`
    },
    body: formData
  });
  
  if (response.ok) {
    const config = await response.json();
    console.log('Configuración creada:', config);
    console.log('QR subido a:', config.qr_url);
  } else {
    console.error('Error:', await response.text());
  }
}

// HTML del formulario
/*
<form id="payment-config-form">
  <input type="file" id="qr-file" accept="image/*" required>
  <input type="text" id="numero-cuenta" required>
  <input type="text" id="banco">
  <input type="text" id="titular">
  <input type="text" id="tipo-cuenta">
  <textarea id="notas"></textarea>
  <button type="submit">Crear Configuración</button>
</form>
*/

// Manejar el formulario
document.getElementById('payment-config-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const fileInput = document.getElementById('qr-file');
  const imageFile = fileInput.files[0];
  
  const data = {
    numero_cuenta: document.getElementById('numero-cuenta').value,
    banco: document.getElementById('banco').value,
    titular: document.getElementById('titular').value,
    tipo_cuenta: document.getElementById('tipo-cuenta').value,
    notas: document.getElementById('notas').value
  };
  
  await createPaymentConfig(imageFile, data);
});

// Obtener y mostrar configuración
async function getAndDisplayPaymentConfig() {
  const response = await fetch('http://localhost:8000/api/v1/payment-config/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    const config = await response.json();
    
    // Mostrar QR
    document.getElementById('qr-image').src = config.qr_url;
    
    // Mostrar datos
    document.getElementById('account-number').textContent = config.numero_cuenta;
    document.getElementById('bank-name').textContent = config.banco;
    document.getElementById('account-holder').textContent = config.titular;
    document.getElementById('account-type').textContent = config.tipo_cuenta;
  } else if (response.status === 404) {
    alert('No hay configuración de pagos disponible. Contacte al administrador.');
  }
}

// Actualizar QR (admin)
async function updatePaymentQR(newImageFile) {
  const formData = new FormData();
  formData.append('file', newImageFile);
  
  const response = await fetch('http://localhost:8000/api/v1/payment-config/', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${adminToken}`
    },
    body: formData
  });
  
  if (response.ok) {
    alert('QR actualizado exitosamente');
    await getAndDisplayPaymentConfig(); // Recargar
  }
}

// Actualizar solo datos (admin)
async function updatePaymentData(data) {
  const formData = new FormData();
  
  if (data.numero_cuenta) formData.append('numero_cuenta', data.numero_cuenta);
  if (data.banco) formData.append('banco', data.banco);
  if (data.titular) formData.append('titular', data.titular);
  if (data.tipo_cuenta) formData.append('tipo_cuenta', data.tipo_cuenta);
  if (data.notas) formData.append('notas', data.notas);
  
  const response = await fetch('http://localhost:8000/api/v1/payment-config/', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${adminToken}`
    },
    body: formData
  });
  
  if (response.ok) {
    alert('Datos actualizados exitosamente');
  }
}
```

---

## ⚠️ IMPORTANTE

### Cambios vs Versión Anterior

**ANTES** (JSON Body):
```json
POST /payment-config/
{
  "numero_cuenta": "...",
  "qr_url": "https://..."  // Admin proporcionaba URL
}
```

**AHORA** (Form Data):
```bash
POST /payment-config/
-F "file=@/path/to/qr.png"  # Sistema sube imagen
-F "numero_cuenta=..."
```

### Ventajas del nuevo sistema:

✅ **Más simple para el frontend**: Solo suben la imagen, no necesitan Cloudinary  
✅ **Más seguro**: El servidor controla la subida  
✅ **Validación automática**: Formato, tamaño, tipo de archivo  
✅ **URL consistente**: Siempre `payment_config/qr_payment`  
✅ **Reemplazo fácil**: PUT con nueva imagen reemplaza la anterior  

---

## 📚 Documentación Completa

Ver archivos:
- `CONFIGURACION_PAGOS.md` - Documentación detallada
- `RESUMEN_CONFIGURACION_PAGOS.md` - Resumen ejecutivo
- `TEST_RESULTS_PAYMENT_CONFIG.md` - Resultados de pruebas

---

**Para más información consulta la documentación Swagger:**
http://localhost:8000/docs
