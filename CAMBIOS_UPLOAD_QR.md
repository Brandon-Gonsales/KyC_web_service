# ✅ ACTUALIZACIÓN COMPLETADA - Upload Directo de QR

## 🎯 Cambio Implementado

El sistema ahora **recibe la imagen del QR directamente** en los endpoints de crear y actualizar, en lugar de recibir solo la URL.

---

## 📝 Cambios Realizados

### 1. **API Modificada** (`api/payment_config.py`)

#### ANTES:
```python
@router.post("/")
async def create_payment_config(
    config_in: PaymentConfigCreate,  # JSON Body
    ...
)
```

#### AHORA:
```python
@router.post("/")
async def create_payment_config(
    file: UploadFile = File(...),  # Imagen del QR
    numero_cuenta: str = Form(...),
    banco: Optional[str] = Form(None),
    ...
)
```

### Características:
✅ Recibe imagen del QR directamente (`multipart/form-data`)  
✅ Sube automáticamente a Cloudinary  
✅ Guarda la URL generada en MongoDB  
✅ Valida formato (JPG, PNG, WEBP)  
✅ Valida tamaño (máximo 5MB)  

---

## 🔄 Flujo Actualizado

### Crear Configuración (POST):
```
1. Admin selecciona imagen QR
2. Frontend envía FormData con imagen + datos
3. Backend valida la imagen
4. Backend sube a Cloudinary → obtiene URL
5. Backend guarda configuración con URL
6. Retorna configuración con qr_url
```

### Actualizar Configuración (PUT):
```
1. Admin puede enviar nueva imagen (opcional)
2. Si envía imagen:
   - Backend sube a Cloudinary
   - Reemplaza imagen anterior
   - Actualiza qr_url
3. Actualiza otros campos si se proporcionan
4. Retorna configuración actualizada
```

---

## 📡 Nuevos Endpoints

### POST /payment-config/ (Crear)
```bash
curl -X POST http://localhost:8000/api/v1/payment-config/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/ruta/a/qr.png" \
  -F "numero_cuenta=1234567890" \
  -F "banco=BNB" \
  -F "titular=UMSA"
```

### PUT /payment-config/ (Actualizar)
```bash
# Solo actualizar número de cuenta
curl -X PUT ... -F "numero_cuenta=9999999999"

# Solo actualizar QR
curl -X PUT ... -F "file=@/ruta/a/nuevo_qr.png"

# Actualizar ambos
curl -X PUT ... \
  -F "file=@/ruta/a/nuevo_qr.png" \
  -F "numero_cuenta=9999999999"
```

---

## 🎨 Frontend - Ejemplo de Uso

### HTML:
```html
<form id="payment-config-form">
  <input type="file" id="qr-file" accept="image/*" required>
  <input type="text" id="numero-cuenta" placeholder="Nº Cuenta" required>
  <input type="text" id="banco" placeholder="Banco">
  <input type="text" id="titular" placeholder="Titular">
  <button type="submit">Crear Configuración</button>
</form>
```

### JavaScript:
```javascript
document.getElementById('payment-config-form')
  .addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('file', document.getElementById('qr-file').files[0]);
    formData.append('numero_cuenta', document.getElementById('numero-cuenta').value);
    formData.append('banco', document.getElementById('banco').value);
    formData.append('titular', document.getElementById('titular').value);
    
    const response = await fetch('/api/v1/payment-config/', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    });
    
    if (response.ok) {
      const config = await response.json();
      console.log('QR subido a:', config.qr_url);
    }
  });
```

---

## ✨ Ventajas

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Upload QR** | Admin subía manualmente a Cloudinary | Sistema sube automáticamente |
| **Content-Type** | `application/json` | `multipart/form-data` |
| **Complejidad Frontend** | Alta (necesita Cloudinary) | Baja (solo sube imagen) |
| **Validación** | Manual | Automática (formato, tamaño) |
| **Seguridad** | Menor (URL externa) | Mayor (servidor controla) |
| **Experiencia** | 2 pasos | 1 paso |

---

## 🛠️ Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `api/payment_config.py` | ✅ Endpoints usan `UploadFile` y `Form` |
| `CURL_EXAMPLES_PAYMENT_CONFIG.md` | ✅ Ejemplos actualizados con `-F` |

---

## ⚠️ IMPORTANTE

### Schemas NO Modificados
Los schemas `PaymentConfigCreate` y `PaymentConfigUpdate` ya **NO se usan** en los endpoints POST y PUT, porque ahora usamos `Form` directamente.

Se mantienen en el código para compatibilidad pero los endpoints nuevos no los necesitan.

### Migración
Si ya existía una configuración con URL manual:
- ✅ Sigue funcionando (GET retorna la URL)  
- ✅ Puede actualizarse con nueva imagen (PUT con file)  
- ✅ No es necesario migrar datos  

---

## 📚 Documentación Actualizada

- ✅ `CURL_EXAMPLES_PAYMENT_CONFIG.md` - Ejemplos completos con FormData  
- ⏳ `CONFIGURACION_PAGOS.md` - Pendiente actualizar  
- ⏳ `RESUMEN_CONFIGURACION_PAGOS.md` - Pendiente actualizar  

---

## 🎉 Estado

```
╔═══════════════════════════════════════════════════╗
║  ✅ UPLOAD DIRECTO DE QR IMPLEMENTADO           ║
╚═══════════════════════════════════════════════════╝

✅ Endpoints modificados (POST, PUT)
✅ Upload automático a Cloudinary
✅ Validación de imágenes
✅ Ejemplos de uso actualizados
✅ Frontend simplificado

🚀 Listo para probar
```

---

**Fecha**: 17 de Diciembre de 2024  
**Sistema**: KyC Payment System API  
**Feature**: Upload Directo de QR a Cloudinary
