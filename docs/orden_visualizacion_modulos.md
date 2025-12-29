# 📊 Orden de Visualización por Módulo - Sistema KyC

**Fecha**: 29 de Diciembre, 2024  
**Propósito**: Documentar el orden en que se muestran los registros en cada módulo

---

## Resumen Ejecutivo

| Módulo | Orden Actual | Campo de Ordenamiento | Más Reciente Primero |
|--------|--------------|----------------------|----------------------|
| **Pagos** | ✅ Descendente | `fecha_subida` | ✅ SÍ |
| **Inscripciones** | ⚠️ Sin ordenar | N/A | ❌ NO |
| **Estudiantes** | ⚠️ Sin ordenar | N/A | ❌ NO |
| **Cursos** | ⚠️ Sin ordenar | N/A | ❌ NO |
| **Usuarios** | ⚠️ Sin ordenar | N/A | ❌ NO |
| **Descuentos** | ⚠️ Sin ordenar | N/A | ❌ NO |

---

## 📋 Detalle por Módulo

### 1. Pagos ✅

**Archivo**: `services/payment_service.py`

**Funciones con ordenamiento**:
- `get_all_payments()` → `.sort("-fecha_subida")` ✅
- `get_payments_by_student()` → `.sort("-fecha_subida")` ✅
- `get_payments_by_enrollment()` → `.sort("-fecha_subida")` ✅
- `get_payments_by_course()` → `.sort("-fecha_subida")` ✅

**Reporte Excel**: `api/payments.py` → `.sort("-fecha_subida")` ✅

**Orden**: **Descendente** (más reciente primero)  
**Campo**: `fecha_subida`

---

### 2. Inscripciones (Enrollments) ⚠️

**Archivo**: `services/enrollment_service.py`

**Función**: `get_all_enrollments()` (línea 241)

**Código actual**:
```python
enrollments = await query.skip(skip).limit(per_page).to_list()
```

**Orden**: **Sin ordenar** (orden de inserción en MongoDB)  
**Recomendación**: Ordenar por `fecha_inscripcion` descendente

---

### 3. Estudiantes (Students) ⚠️

**Archivo**: `services/student_service.py`

**Función**: `get_all_students()` (línea 84)

**Código actual**:
```python
students = await query.skip(skip).limit(per_page).to_list()
```

**Orden**: **Sin ordenar** (orden de inserción en MongoDB)  
**Recomendación**: Ordenar por `created_at` descendente o `nombre` alfabético

---

### 4. Cursos (Courses) ⚠️

**Archivo**: `services/course_service.py`

**Función**: `get_all_courses()` (línea 67)

**Código actual**:
```python
courses = await query.skip(skip).limit(per_page).to_list()
```

**Orden**: **Sin ordenar** (orden de inserción en MongoDB)  
**Recomendación**: Ordenar por `created_at` descendente o `nombre_programa` alfabético

---

### 5. Usuarios (Users) ⚠️

**Archivo**: `services/user_service.py`

**Función**: `get_all_users()` (línea 22)

**Código actual**:
```python
users = await query.skip(skip).limit(per_page).to_list()
```

**Orden**: **Sin ordenar** (orden de inserción en MongoDB)  
**Recomendación**: Ordenar por `created_at` descendente o `username` alfabético

---

### 6. Descuentos (Discounts) ⚠️

**Archivo**: `services/discount_service.py`

**Función**: `get_all_discounts()` (línea 19)

**Código actual**:
```python
discounts = await query.skip(skip).limit(per_page).to_list()
```

**Orden**: **Sin ordenar** (orden de inserción en MongoDB)  
**Recomendación**: Ordenar por `created_at` descendente

---

## 🎯 Recomendaciones de Ordenamiento

### Opción A: Todos por Fecha de Creación (Más Reciente Primero)

**Ventaja**: Consistencia total, siempre ves lo más nuevo primero

| Módulo | Campo | Orden |
|--------|-------|-------|
| Pagos | `fecha_subida` | `-fecha_subida` ✅ (ya implementado) |
| Inscripciones | `fecha_inscripcion` | `-fecha_inscripcion` |
| Estudiantes | `created_at` | `-created_at` |
| Cursos | `created_at` | `-created_at` |
| Usuarios | `created_at` | `-created_at` |
| Descuentos | `created_at` | `-created_at` |

---

### Opción B: Orden Mixto (Según Contexto)

**Ventaja**: Más intuitivo según el tipo de dato

| Módulo | Campo | Orden | Razón |
|--------|-------|-------|-------|
| Pagos | `fecha_subida` | Descendente ✅ | Lo más reciente es más relevante |
| Inscripciones | `fecha_inscripcion` | Descendente | Inscripciones nuevas primero |
| Estudiantes | `nombre` | Alfabético (A-Z) | Fácil de buscar por nombre |
| Cursos | `nombre_programa` | Alfabético (A-Z) | Fácil de buscar por nombre |
| Usuarios | `username` | Alfabético (A-Z) | Fácil de buscar por username |
| Descuentos | `created_at` | Descendente | Descuentos nuevos primero |

---

## 🔧 Implementación Sugerida

### Para ordenar por fecha descendente:

```python
# Ejemplo: Inscripciones
enrollments = await query.sort("-fecha_inscripcion").skip(skip).limit(per_page).to_list()
```

### Para ordenar alfabéticamente:

```python
# Ejemplo: Estudiantes
students = await query.sort("+nombre").skip(skip).limit(per_page).to_list()
```

**Nota**: 
- `+` = Ascendente (A-Z, 0-9, más antiguo primero)
- `-` = Descendente (Z-A, 9-0, más reciente primero)

---

## ⚡ Acción Recomendada

**Pregunta para el equipo**: ¿Qué orden prefieren?

1. **Opción A**: Todo por fecha (más reciente primero)
2. **Opción B**: Mixto (fechas descendentes, nombres alfabéticos)
3. **Personalizado**: Especificar orden por cada módulo

Una vez decidido, puedo implementar el ordenamiento en todos los módulos.

---

**Elaborado por**: Equipo Backend  
**Última actualización**: 29 de Diciembre, 2024
