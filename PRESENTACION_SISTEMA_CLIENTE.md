# 📚 Sistema de Gestión de Cursos y Diplomados - KYC
## Presentación Ejecutiva para el Cliente

---

## 🎯 ¿Qué es el Sistema?

**KYC** es una plataforma web integral para la **gestión completa de cursos, diplomados y programas de formación**, diseñada específicamente para instituciones educativas que necesitan administrar eficientemente:

- ✅ Inscripciones de estudiantes
- ✅ Pagos y cuotas
- ✅ Documentación y requisitos
- ✅ Control financiero
- ✅ Reportes y seguimiento

---

## 💼 Problemas que Resuelve

### Antes del Sistema:
❌ Registro manual de estudiantes en planillas Excel  
❌ Control de pagos desorganizado  
❌ Requisitos en carpetas físicas o archivos dispersos  
❌ Dificultad para hacer seguimiento de deudores  
❌ Imposibilidad de generar reportes rápidos  
❌ Errores humanos en cálculos de descuentos  

### Con el Sistema:
✅ **Registro digital centralizado** de todos los estudiantes  
✅ **Control automático de pagos** con validación  
✅ **Gestión digital de documentos** en la nube  
✅ **Seguimiento en tiempo real** de pagos pendientes  
✅ **Reportes automáticos** en Excel  
✅ **Cálculos precisos** de descuentos y cuotas  

---

## 👥 Tipos de Usuarios del Sistema

### 1. 🎓 **Estudiantes**
- Pueden ver sus cursos inscritos
- Suben comprobantes de pago
- Suben documentos requisitos
- Ven su progreso de pagos
- Cambian su contraseña

### 2. 👨‍💼 **Administradores**
- Gestionan cursos y estudiantes
- Aprueban o rechazan pagos
- Revisan documentos requisitos
- Generan reportes
- Configuran descuentos
- Control total del sistema

### 3. 👤 **Super Administradores**
- Todo lo del Admin +
- Crean/eliminan otros administradores
- Eliminan cursos y descuentos
- Configuración avanzada

---

## 🔄 Flujos Principales del Sistema

### 📝 FLUJO 1: Inscripción de un Estudiante

```
1. ADMIN → Crea el curso con requisitos
          ↓
2. ADMIN → Registra al estudiante en el sistema
          ↓
3. ADMIN → Inscribe al estudiante en el curso
          ↓
   SISTEMA → Calcula automáticamente:
             • Precio según tipo (interno/externo)
             • Descuentos aplicables
             • Monto de matrícula
             • Número de cuotas
             • Total a pagar
          ↓
4. SISTEMA → Copia requisitos del curso al enrollment
          ↓
✅ Estudiante inscrito y listo para pagar
```

### 💰 FLUJO 2: Proceso de Pago

```
1. ESTUDIANTE → Realiza depósito bancario
              ↓
2. ESTUDIANTE → Sube comprobante al sistema
                • Foto/PDF del voucher
                • Número de transacción
              ↓
   SISTEMA → Estado: "PENDIENTE"
              ↓
3. ADMIN → Recibe notificación de pago pendiente
         ↓
4. ADMIN → Revisa el comprobante
         ↓
         ┌─────────────┬─────────────┐
         ↓             ↓             ↓
    APROBAR       RECHAZAR      (nada)
         ↓             ↓             
   Estado:        Estado:        Estado:
   APROBADO       RECHAZADO      PENDIENTE
         ↓             ↓
   Saldo se      Estudiante
   actualiza     debe resubir
         ↓
✅ Pago registrado correctamente
```

### 📄 FLUJO 3: Gestión de Requisitos/Documentos

```
1. ADMIN → Define requisitos al crear curso
          Ejemplos:
          • CV actualizado
          • Fotocopia de CI
          • Título profesional
          ↓
2. Al inscribir → Requisitos se copian automáticamente
          ↓
3. ESTUDIANTE → Sube documentos uno por uno
              ↓
   SISTEMA → Estado: "EN PROCESO"
              ↓
4. ADMIN → Revisa cada documento
         ↓
         ┌─────────────┬─────────────┐
         ↓             ↓             
    APROBAR       RECHAZAR
                  (con motivo)
         ↓             ↓
   Estado:        Estado:
   APROBADO       RECHAZADO
                      ↓
              Estudiante ve motivo
              y puede resubir
                      ↓
✅ Documentación completa y verificada
```

---

## 🎁 Sistema Inteligente de Descuentos

### Tipos de Descuentos:

#### 1. **Descuento del Curso** (Automático)
- Se aplica a TODOS los estudiantes del curso
- Ejemplo: "Descuento Promocional 10%"
- El admin lo configura en el curso

#### 2. **Descuento Personalizado** (Individual)
- Se aplica solo a estudiantes específicos
- Ejemplo: "Beca Excelencia 30%" para Juan Pérez
- Se asigna al momento de inscribir

### ⚙️ Cálculo Automático (Doble Descuento):

```
Precio Base: 3,500 Bs

1. Aplica descuento del curso (10%)
   3,500 - 350 = 3,150 Bs

2. Aplica descuento personalizado (5%)
   3,150 - 157.50 = 2,992.50 Bs

✅ TOTAL A PAGAR: 2,992.50 Bs
```

**El sistema hace TODOS estos cálculos automáticamente** ✨

---

## 📊 Módulos del Sistema

### 1. 📚 **Gestión de Cursos**
- Crear cursos con toda la información
- Definir precios diferenciados (interno/externo)
- Configurar cuotas y descuentos
- Definir requisitos documentales
- Ver estudiantes inscritos
- Activar/desactivar cursos

### 2. 🎓 **Gestión de Estudiantes**
- Registro completo de estudiantes
- Tipo: Interno o Externo (afecta precio)
- Foto de perfil
- Información de contacto
- Historial de cursos
- Cambio de contraseña

### 3. 📝 **Inscripciones (Enrollments)**
- Inscribir estudiantes en cursos
- Asignación automática de precios
- Aplicación de descuentos
- Control de saldos
- Estado de la inscripción
- Notas finales

### 4. 💳 **Gestión de Pagos**
- Registro de pagos con comprobante
- Validación por administradores
- Estados: Pendiente, Aprobado, Rechazado
- Cálculo automático de cuotas
- Historial completo
- **📊 Reporte Excel diario**

### 5. 📄 **Requisitos y Documentos**
- Gestión digital de documentación
- Almacenamiento en la nube (Cloudinary)
- Estados: Pendiente, En Proceso, Aprobado, Rechazado
- Feedback al estudiante
- Resubida de documentos rechazados
- Estadísticas de progreso

### 6. 🎁 **Descuentos**
- Crear descuentos predefinidos
- Asignar a cursos o estudiantes
- Cálculo automático en cascada
- Control de vigencia

### 7. ⚙️ **Configuración de Pagos**
- QR de pago institucional
- Datos bancarios
- Información que verán los estudiantes
- Actualización dinámica

---

## 📈 Características Destacadas

### 🤖 **Automatización Inteligente**

#### Cálculo Automático de Próximo Pago:
- El sistema **sabe** qué debe pagar el estudiante
- Sugiere el concepto (Matrícula, Cuota 1, Cuota 2...)
- Calcula el monto exacto
- El estudiante solo confirma

#### Validación Estricta:
```
Estudiante intenta pagar:
❌ Monto incorrecto → RECHAZADO
❌ Concepto equivocado → RECHAZADO  
❌ Cuota fuera de orden → RECHAZADO
✅ Todo correcto → ACEPTADO
```

### 📊 **Reportes y Estadísticas**

#### Reporte Diario de Pagos (Excel):
Columnas:
- Nombre del estudiante
- Fecha y hora
- Moneda (Bs)
- Monto
- Concepto
- N° de transacción
- Estado
- **Progreso** (ej: 7/12 cuotas pagadas)

**Ideal para:**
- Cruce con datos bancarios
- Contabilidad
- Auditorías

#### Panel de Información:
- Pagos pendientes de revisión
- Requisitos por aprobar
- Saldo total pendiente
- Estadísticas por curso

### 🔐 **Seguridad y Permisos**

✅ **Autenticación JWT** (tokens seguros)  
✅ **Roles y permisos** estrictos  
✅ **Passwords encriptados**  
✅ **Acceso controlado** por endpoints  
✅ **Logging de acciones** importantes  

### ☁️ **Almacenamiento en la Nube**

Todos los archivos (comprobantes, requisitos, fotos) se almacenan en **Cloudinary**:
- ✅ Acceso rápido desde cualquier lugar
- ✅ Respaldo automático
- ✅ Sin límite de almacenamiento
- ✅ URLs permanentes

---

## 🎯 Ventajas Competitivas

| Antes | Ahora con KYC |
|-------|---------------|
| Excel manual | Base de datos profesional |
| Carpetas físicas | Documentos digitales en la nube |
| Cálculos manuales | Cálculos automáticos precisos |
| Sin historial | Trazabilidad completa |
| Reportes lentos | Reportes instantáneos |
| Propenso a errores | Validación automática |
| Acceso local | Acceso desde cualquier lugar |

---

## 💡 Casos de Uso Reales

### Escenario 1: Inscripción con Beca
```
1. Admin crea "Diplomado ISO 9001" - Precio: 3,500 Bs
2. Estudiante Juan tiene beca del 30%
3. Admin inscribe a Juan
4. Sistema calcula: 3,500 - 1,050 = 2,450 Bs
5. Juan paga en 5 cuotas de 490 Bs
```

### Escenario 2: Pago Rechazado
```
1. Estudiante María sube comprobante borroso
2. Admin rechaza: "Imagen ilegible"
3. María ve el motivo en su panel
4. María resubmite foto clara
5. Admin aprueba ✅
```

### Escenario 3: Control de Requisitos
```
Estudiante tiene 4 requisitos:
✅ CV - APROBADO
🔄 CI - EN REVISIÓN
❌ Título - RECHAZADO (falta firma)
⏳ Certificado - PENDIENTE

Progreso: 25% completado
```

---

## 📱 Interfaz y Experiencia

### Para el Estudiante:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Mis Cursos

Diplomado ISO 9001
💰 Pagos: 7/12 cuotas (58%)
📄 Requisitos: 3/4 aprobados

[Ver Detalle] [Subir Pago]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Para el Administrador:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Panel de Control

⏳ 5 pagos pendientes
📄 3 requisitos por revisar
💰 Total pendiente: 45,230 Bs
👥 15 estudiantes activos

[Ver Pagos] [Generar Reporte]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 Tecnología

### Backend (API):
- **Python** + **FastAPI** (Alto rendimiento)
- **MongoDB** (Base de datos escalable)
- **JWT** (Autenticación segura)
- **Cloudinary** (Almacenamiento en la nube)

### Características Técnicas:
✅ API RESTful documentada (Swagger)  
✅ Arquitectura modular y escalable  
✅ Validaciones automáticas  
✅ Respuestas en JSON  
✅ Compatible con cualquier frontend  

---

## 📖 Documentación Técnica

El sistema incluye **documentación Swagger automática** accessible en:
```
http://tu-servidor/docs
```

Permite:
- ✅ Ver todos los endpoints
- ✅ Probar la API directamente
- ✅ Ver ejemplos de peticiones
- ✅ Entender respuestas

---

## 🚀 Próximos Pasos

### Para Implementar:
1. Configurar servidor (puede ser local o en la nube)
2. Configurar base de datos MongoDB
3. Configurar Cloudinary para archivos
4. Crear usuario Super Administrador inicial
5. Desarrollar frontend (web/móvil)

### Capacitación Sugerida:
- ✅ Administradores: 2 horas
- ✅ Personal de finanzas: 1 hora
- ✅ Estudiantes: Tutorial en video (15 min)

---

## 📞 Soporte

El sistema está diseñado para:
- ✅ Ser intuitivo y fácil de usar
- ✅ Minimizar errores con validaciones
- ✅ Proveer mensajes claros
- ✅ Facilitar el soporte técnico

---

## ✨ Resumen Ejecutivo

**KYC** es una solución completa que **digitaliza y automatiza** la gestión de cursos, eliminando el trabajo manual, reduciendo errores y proporcionando control total sobre:

- 📚 **Cursos y programas**
- 🎓 **Estudiantes**
- 💰 **Finanzas y pagos**
- 📄 **Documentación**
- 📊 **Reportes**

**Resultado:** Más eficiencia, menos errores, mejor servicio a los estudiantes.

---

**Desarrollado por:** Tu Equipo de Desarrollo  
**Fecha:** Diciembre 2024  
**Versión:** 1.0

---

## 🎯 ¿Por qué elegir KYC?

✅ **Ahorro de tiempo**: Lo que tomaba horas, ahora toma minutos  
✅ **Precisión**: Cero errores en cálculos  
✅ **Transparencia**: Todo registrado y trazable  
✅ **Escalabilidad**: Crece con tu institución  
✅ **Profesionalismo**: Sistema moderno y confiable  

---

*¿Listo para transformar la gestión de tu institución educativa?*
