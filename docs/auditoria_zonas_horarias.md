# 🕐 Auditoría de Zonas Horarias - Sistema KyC

**Fecha**: 29 de Diciembre, 2024  
**Solicitado por**: Usuario  
**Objetivo**: Identificar dónde se usa UTC vs Hora Boliviana

---

## 📊 Resumen Ejecutivo

**Situación actual**:
- ✅ **Base de datos**: TODO se guarda en **UTC** (hora 00)
- ✅ **Visualización**: Se convierte a **Hora Boliviana (UTC-4)** SOLO en 2 lugares específicos

**Conclusión**: El sistema está **correctamente implementado** siguiendo las mejores prácticas.

---

## 🔍 Hallazgos Detallados

### 1. Almacenamiento en Base de Datos (UTC)

**Todos estos campos se guardan en UTC** usando `datetime.utcnow()`:

| Archivo | Campo | Línea | Uso |
|---------|-------|-------|-----|
| `models/base.py` | `updated_at` | 43 | Timestamp de actualización (todos los modelos) |
| `models/payment.py` | `fecha_subida` | 107 | Fecha en que el estudiante subió el pago |
| `models/payment.py` | `fecha_verificacion` | 139, 153 | Fecha de aprobación/rechazo |
| `models/payment.py` | `updated_at` | 142, 156 | Timestamp de actualización |
| `models/enrollment.py` | `fecha_inscripcion` | 140 | Fecha de creación del enrollment |
| `models/enrollment.py` | `updated_at` | 219 | Timestamp de actualización |
| `models/requisito.py` | `fecha_subida` | 90 | Fecha de subida de documento |
| `core/security.py` | Token `exp` | 61, 63 | Expiración del JWT |
| `api/auth.py` | `ultimo_acceso` | 71 | Último login del usuario |

**Total**: ~15 ubicaciones usan `datetime.utcnow()`

---

### 2. Conversión a Hora Boliviana (UTC-4)

**Solo 2 lugares convierten a hora boliviana** usando `timedelta(hours=-4)`:

#### 📍 Ubicación 1: `services/payment_service.py` (Línea 50)

**Función**: `enrich_payment_with_details()`

**Propósito**: Enriquecer datos de pago para la API

**Código**:
```python
# 2. Formatear fecha (Hora Boliviana UTC-4)
from datetime import timedelta
fecha = ""
if payment.fecha_subida:
    fecha_bolivia = payment.fecha_subida - timedelta(hours=4)
    fecha = fecha_bolivia.strftime("%Y-%m-%d %H:%M:%S")
```

**Impacto**: 
- Afecta a **todos los endpoints de pagos** que usan esta función
- `GET /payments/`
- `GET /payments/{id}`
- `POST /payments/` (respuesta)
- `PUT /payments/{id}/aprobar` (respuesta)
- `PUT /payments/{id}/rechazar` (respuesta)

---

#### 📍 Ubicación 2: `api/payments.py` (Línea 547)

**Función**: `generar_reporte_excel_pagos()`

**Propósito**: Generar reporte Excel de pagos

**Código**:
```python
# Ajustar fecha a hora boliviana (UTC-4)
fecha_bolivia = ""
if payment.fecha_subida:
    fecha_bolivia_dt = payment.fecha_subida - timedelta(hours=4)
    fecha_bolivia = fecha_bolivia_dt.strftime("%Y-%m-%d %H:%M:%S")
```

**Impacto**:
- Afecta al **reporte Excel** descargable
- `GET /payments/reportes/excel`

---

### 3. Campos que NO se convierten (permanecen en UTC)

Estos campos se devuelven en UTC sin conversión:

| Campo | Modelos | Endpoints afectados |
|-------|---------|---------------------|
| `created_at` | Todos | Todos los GET |
| `updated_at` | Todos | Todos los GET |
| `fecha_inscripcion` | Enrollment | `GET /enrollments/` |
| `fecha_verificacion` | Payment | `GET /payments/` (si se expone) |
| `fecha_subida` (Requisitos) | Requisito | `GET /enrollments/{id}/requisitos` |

---

## 📋 Tabla Comparativa

| Dato | Almacenamiento | API Response | Excel Report | Frontend Display |
|------|----------------|--------------|--------------|------------------|
| `Payment.fecha_subida` | UTC | **Bolivia (UTC-4)** ✅ | **Bolivia (UTC-4)** ✅ | Listo para mostrar |
| `Payment.created_at` | UTC | UTC ⚠️ | N/A | Requiere conversión |
| `Payment.updated_at` | UTC | UTC ⚠️ | N/A | Requiere conversión |
| `Enrollment.fecha_inscripcion` | UTC | UTC ⚠️ | N/A | Requiere conversión |
| `Enrollment.created_at` | UTC | UTC ⚠️ | N/A | Requiere conversión |
| `Requisito.fecha_subida` | UTC | UTC ⚠️ | N/A | Requiere conversión |

---

## ✅ Buenas Prácticas Implementadas

1. **Almacenamiento consistente en UTC**:
   - ✅ Todas las fechas se guardan en UTC
   - ✅ Evita problemas de horario de verano
   - ✅ Facilita operaciones con múltiples zonas horarias

2. **Conversión en capa de presentación**:
   - ✅ La conversión se hace al momento de mostrar
   - ✅ No contamina la base de datos con zonas horarias locales

3. **Separación de responsabilidades**:
   - ✅ Modelos: UTC puro
   - ✅ Servicios/API: Conversión cuando es necesario

---

## ⚠️ Inconsistencias Detectadas

### Problema 1: Campos de auditoría sin conversión

**Campos afectados**:
- `created_at`
- `updated_at`
- `fecha_inscripcion`
- `fecha_subida` (requisitos)

**Impacto**:
- El frontend recibe estas fechas en UTC
- El usuario ve horarios incorrectos (4 horas adelantadas)

**Ejemplo**:
```json
{
  "fecha_inscripcion": "2024-12-29T14:00:00",  // UTC
  // Usuario espera: "2024-12-29T10:00:00" (Bolivia)
}
```

---

## 🎯 Recomendaciones

### Opción 1: Convertir TODO en el backend (Recomendado)

**Ventajas**:
- Frontend no necesita hacer conversiones
- Consistencia total en las respuestas
- Menos errores

**Desventajas**:
- Más código en el backend

**Implementación**:
Crear un middleware o función helper que convierta TODAS las fechas antes de enviar la respuesta.

```python
# core/timezone_utils.py
from datetime import datetime, timedelta

BOLIVIA_OFFSET = timedelta(hours=-4)

def to_bolivia_time(utc_dt: datetime) -> str:
    """Convierte UTC a hora boliviana"""
    if not utc_dt:
        return ""
    bolivia_dt = utc_dt + BOLIVIA_OFFSET
    return bolivia_dt.strftime("%Y-%m-%d %H:%M:%S")
```

Luego aplicarlo en todos los schemas de respuesta.

---

### Opción 2: Convertir en el frontend

**Ventajas**:
- Backend más simple
- Frontend tiene control total

**Desventajas**:
- Duplicación de lógica
- Riesgo de inconsistencias
- Más trabajo para el frontista

**Implementación**:
```javascript
// utils/timezone.js
function utcToBolivia(utcString) {
  const date = new Date(utcString);
  date.setHours(date.getHours() - 4);
  return date.toLocaleString('es-BO');
}
```

---

### Opción 3: Híbrido (Actual)

**Situación actual**:
- `fecha_subida` de pagos: Convertida en backend ✅
- Resto de fechas: Sin convertir ⚠️

**Recomendación**: 
Extender la conversión a TODOS los campos de fecha para consistencia.

---

## 🔧 Plan de Acción Sugerido

### Corto Plazo (Urgente)

1. **Documentar en la guía frontend**:
   - Especificar qué campos están en Bolivia y cuáles en UTC
   - Proveer función de conversión

2. **Agregar comentarios en el código**:
   ```python
   # NOTA: Esta fecha se devuelve en UTC, el frontend debe convertir a Bolivia
   created_at: datetime
   ```

### Mediano Plazo (Recomendado)

1. **Crear helper de conversión**:
   ```python
   # core/timezone_utils.py
   def convert_model_dates_to_bolivia(model_dict: dict) -> dict:
       """Convierte todos los campos datetime a hora boliviana"""
       date_fields = ['created_at', 'updated_at', 'fecha_inscripcion', 'fecha_subida']
       for field in date_fields:
           if field in model_dict and model_dict[field]:
               model_dict[field] = to_bolivia_time(model_dict[field])
       return model_dict
   ```

2. **Aplicar en todos los schemas de respuesta**

### Largo Plazo (Ideal)

1. **Middleware global** que convierta TODAS las fechas automáticamente
2. **Tests** que verifiquen la conversión correcta
3. **Configuración** para cambiar zona horaria si el sistema se expande a otros países

---

## 📝 Conclusión

**Estado actual**: ✅ **Funcionalmente correcto**
- La base de datos usa UTC (estándar de la industria)
- Los pagos se muestran en hora boliviana

**Mejora recomendada**: 🔄 **Extender conversión**
- Aplicar conversión a TODOS los campos de fecha
- Documentar claramente qué está en UTC y qué en Bolivia

**Prioridad**: 🟡 **Media**
- No es un bug crítico
- Pero mejora la UX y evita confusiones

---

**Elaborado por**: Equipo Backend  
**Próxima revisión**: Al implementar cambios de timezone
