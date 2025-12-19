# Plan de Actualización de json_schema_extra
# ==========================================

## 🎯 OBJETIVO
Actualizar todos los ejemplos de schemas para que Swagger muestre datos realistas y útiles para el frontend.

---

## 📊 INVENTARIO DE SCHEMAS POR MÓDULO

### 1. AUTH (schemas/auth.py)
- [x] LoginRequest - YA ESTÁ BIEN ✅
- [x] TokenResponse - YA ESTÁ BIEN ✅
- [x] CurrentUserResponse - YA ESTÁ BIEN ✅

**Estado:** 3/3 completados ✅

---

### 2. STUDENTS (schemas/student.py)
Prioridad: 🔴 CRÍTICA

- [ ] StudentCreate (para registro de estudiantes)
- [ ] StudentResponse (respuesta con datos)
- [ ] StudentUpdate (actualización de datos)
- [ ] StudentUpdateSelf (estudiante actualiza su perfil)
- [ ] StudentUpdateAdmin (admin actualiza estudiante)
- [ ] ChangePassword (cambio de contraseña)

**Total:** 6 schemas
**Tiempo estimado:** 20 minutos

**Ejemplos a mejorar:**
```python
# ANTES (genérico)
"registro": "string"
"nombre": "string" 
"email": "string"

# DESPUÉS (realista)
"registro": "20240001"
"nombre": "Juan Carlos Pérez López"
"email": "juan.perez@estudiante.edu.bo"
"carnet": "12345678"
"extension": "LP"
"celular": "70123456"
"tipo_estudiante": "interno"
```

---

### 3. ENROLLMENTS (schemas/enrollment.py)
Prioridad: 🔴 CRÍTICA

- [ ] EnrollmentCreate (crear inscripción)
- [ ] EnrollmentResponse (respuesta completa)
- [ ] EnrollmentUpdate (actualizar inscripción)
- [ ] NextPaymentInfo (próximo pago)

**Total:** 4 schemas
**Tiempo estimado:** 25 minutos

**Ejemplos clave:**
```python
"estudiante_id": "507f1f77bcf86cd799439011"
"curso_id": "507f1f77bcf86cd799439012"
"descuento_personalizado": 10.0
"nota_final": 85.5
```

---

### 4. PAYMENTS (schemas/payment.py)
Prioridad: 🔴 CRÍTICA

- [ ] PaymentCreate (registrar pago)
- [ ] PaymentResponse (respuesta de pago)
- [ ] PaymentApproval (aprobar pago)
- [ ] PaymentRejection (rechazar pago)
- [ ] PaymentWithDetails (pago con detalles)

**Total:** 5 schemas
**Tiempo estimado:** 20 minutos

**Ejemplos importantes:**
```python
"inscripcion_id": "507f1f77bcf86cd799439013"
"numero_transaccion": "TRX-2024-001234"
"comprobante_url": "https://res.cloudinary.com/..."
"monto_pagado": 1500.00
"concepto": "Matrícula"
```

---

### 5. COURSES (schemas/course.py)
Prioridad: 🟡 ALTA

- [ ] CourseCreate (crear curso)
- [ ] CourseResponse (respuesta de curso)
- [ ] CourseUpdate (actualizar curso)
- [ ] CourseEnrolledStudent (estudiante inscrito)

**Total:** 4 schemas
**Tiempo estimado:** 20 minutos

**Ejemplos:**
```python
"nombre": "Diplomado en Certificación de Sistemas de Gestión"
"codigo": "DIP-CSG-2024"
"tipo_curso": "diplomado"
"modalidad": "hibrido"
"precio_interno": 3000.00
"precio_externo": 3500.00
"descuento_curso": 10.0
"duracion_meses": 6
```

---

### 6. REQUISITOS (schemas/requisito.py)
Prioridad: 🟡 ALTA

- [ ] RequisitoBase (base de requisito)
- [ ] RequisitoResponse (respuesta)
- [ ] RequisitoRechazarRequest (rechazar requisito)
- [ ] RequisitoListResponse (lista con stats)

**Total:** 4 schemas
**Tiempo estimado:** 15 minutos

**Ejemplos:**
```python
"descripcion": "Fotocopia de Carnet de Identidad"
"estado": "aprobado"
"url": "https://res.cloudinary.com/..."
"motivo_rechazo": "Imagen borrosa, no se lee el número"
```

---

### 7. PAYMENT CONFIG (schemas/payment_config.py)
Prioridad: 🟢 MEDIA

- [ ] PaymentConfigResponse (configuración de pago)

**Total:** 1 schema
**Tiempo estimado:** 5 minutos

**Ejemplo:**
```python
"numero_cuenta": "1234567890"
"banco": "Banco Nacional de Bolivia"
"titular": "INSTITUTO KYC"
"tipo_cuenta": "Cuenta Corriente"
"qr_url": "https://res.cloudinary.com/..."
```

---

### 8. USERS (schemas/user.py)
Prioridad: 🟢 MEDIA

- [ ] UserCreate (crear usuario admin)
- [ ] UserResponse (respuesta)
- [ ] UserUpdate (actualizar)

**Total:** 3 schemas
**Tiempo estimado:** 10 minutos

**Ejemplo:**
```python
"username": "admin.sistemas"
"email": "admin@kyc.edu.bo"
"nombre_completo": "Administrador del Sistema"
"rol": "admin"
```

---

### 9. DISCOUNTS (schemas/discount.py)
Prioridad: 🟢 BAJA

- [ ] DiscountCreate
- [ ] DiscountResponse
- [ ] DiscountUpdate

**Total:** 3 schemas
**Tiempo estimado:** 10 minutos

---

### 10. COMMON (schemas/common.py)
Prioridad: 🟢 BAJA

- [ ] PaginationMeta (metadatos de paginación)
- [ ] PaginatedResponse (respuesta paginada)

**Total:** 2 schemas
**Tiempo estimado:** 5 minutos

---

## 📈 RESUMEN TOTAL

| Módulo | Schemas | Prioridad | Tiempo Est. | Estado |
|--------|---------|-----------|-------------|--------|
| Auth | 3 | ✅ | - | COMPLETO |
| Students | 6 | 🔴 | 20 min | Pendiente |
| Enrollments | 4 | 🔴 | 25 min | Pendiente |
| Payments | 5 | 🔴 | 20 min | Pendiente |
| Courses | 4 | 🟡 | 20 min | Pendiente |
| Requisitos | 4 | 🟡 | 15 min | Pendiente |
| Payment Config | 1 | 🟢 | 5 min | Pendiente |
| Users | 3 | 🟢 | 10 min | Pendiente |
| Discounts | 3 | 🟢 | 10 min | Pendiente |
| Common | 2 | 🟢 | 5 min | Pendiente |
| **TOTAL** | **35** | - | **~2.5 hrs** | **3/35** |

---

## 🎯 ESTRATEGIA RECOMENDADA

### OPCIÓN A: Por Prioridad (Recomendado)
1. **Fase 1 - CRÍTICOS** (🔴): Students, Enrollments, Payments (65 min)
2. **Fase 2 - ALTOS** (🟡): Courses, Requisitos (35 min)
3. **Fase 3 - MEDIOS/BAJOS** (🟢): Users, Payment Config, Discounts, Common (30 min)

### OPCIÓN B: Por Módulo Completo
Ir módulo por módulo hasta completar todos.

### OPCIÓN C: Solo Críticos
Actualizar solo fase 1 (15 schemas) y dejar el resto como está.

---

## 🛠️ METODOLOGÍA DE ACTUALIZACIÓN

Para cada schema:

1. **Identificar campos** del modelo
2. **Usar datos realistas** bolivianos/locales
3. **Validar tipos** (strings, numbers, booleans, dates)
4. **Verificar IDs** (usar ObjectIds válidos de 24 hex chars)
5. **Usar enums correctos** (estados, roles, tipos)
6. **Probar en Swagger** después de cada módulo

---

## 📋 CHECKLIST DE CALIDAD

Cada ejemplo debe:
- ✅ Usar nombres bolivianos realistas
- ✅ Usar extensiones bolivianas (LP, CB, SC, etc.)
- ✅ Usar formatos de carnet válidos (7-8 dígitos)
- ✅ Usar emails con dominio .bo
- ✅ Usar números de celular bolivianos (8 dígitos, empiezan con 6 o 7)
- ✅ Usar montos en bolivianos (Bs)
- ✅ Usar fechas en formato ISO 8601
- ✅ Usar ObjectIds válidos (24 caracteres hexadecimales)

---

## 🚀 PRÓXIMOS PASOS

1. **Decidir estrategia:** ¿A, B o C?
2. **Empezar por el primer módulo** según la estrategia
3. **Actualizar schema por schema**
4. **Probar en Swagger** cada módulo completado
5. **Marcar como completado** en este plan

---

## 📝 NOTAS

- Los schemas de **Response** suelen heredar/usar los mismos ejemplos que **Create**
- Algunos schemas tienen **múltiples ejemplos** para casos de uso diferentes
- Los **enums** deben usar valores válidos del sistema
- Verificar que los ejemplos sean **consistentes** entre módulos relacionados

---

**Autor:** Antigravity AI
**Fecha:** 2025-12-19
**Versión:** 1.0
