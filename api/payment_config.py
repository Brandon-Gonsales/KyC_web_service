"""
API de Configuración de Pagos
==============================

Endpoints para gestionar la configuración de pagos del sistema (QR y cuenta bancaria).

Permisos:
---------
- POST /payment-config/: ADMIN/SUPERADMIN
- GET /payment-config/: Cualquier usuario autenticado
- PUT /payment-config/: ADMIN/SUPERADMIN
- DELETE /payment-config/: ADMIN/SUPERADMIN

IMPORTANTE: Solo puede existir UNA configuración activa a la vez (singleton).
"""

from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from models.user import User
from models.student import Student
from models.payment_config import PaymentConfig
from schemas.payment_config import PaymentConfigResponse
from services import payment_config_service
from api.dependencies import require_admin, get_current_user

router = APIRouter()


@router.post("/", response_model=PaymentConfigResponse, status_code=201)
async def create_payment_config(
    *,
    file: UploadFile = File(..., description="Imagen del QR de pago (JPG, PNG, WEBP)"),
    numero_cuenta: str = Form(..., description="Número de cuenta bancaria"),
    banco: Optional[str] = Form(None, description="Nombre del banco"),
    titular: Optional[str] = Form(None, description="Titular de la cuenta"),
    tipo_cuenta: Optional[str] = Form(None, description="Tipo de cuenta (Ahorro, Corriente, etc.)"),
    notas: Optional[str] = Form(None, description="Notas adicionales"),
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Crear la configuración de pagos del sistema (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    Content-Type: multipart/form-data
    
    IMPORTANTE: Solo puede existir una configuración activa.
    Si ya existe una, se debe actualizar en lugar de crear.
    
    El admin debe proporcionar:
    - file: Imagen del QR (JPG, PNG, WEBP, máximo 5MB)
    - numero_cuenta: Número de cuenta bancaria
    - banco, titular, tipo_cuenta: Información adicional (opcional)
    
    El sistema automáticamente:
    1. Valida la imagen
    2. Sube la imagen a Cloudinary
    3. Guarda la URL generada
    4. Almacena la configuración en MongoDB
    
    Esta información será visible para todos los usuarios autenticados
    al momento de realizar pagos.
    """
    from core.cloudinary_utils import upload_image
    
    try:
        # Verificar que no exista ya una configuración
        existing = await payment_config_service.get_payment_config()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una configuración de pagos activa. Use PUT para actualizar."
            )
        
        # Subir imagen del QR a Cloudinary
        folder = "payment_config"
        public_id = "qr_payment"
        qr_url = await upload_image(file, folder, public_id)
        
        # Crear configuración
        config = PaymentConfig(
            numero_cuenta=numero_cuenta,
            banco=banco,
            titular=titular,
            tipo_cuenta=tipo_cuenta,
            qr_url=qr_url,
            notas=notas,
            creado_por=current_user.username,
            actualizado_por=current_user.username,
            is_active=True
        )
        
        await config.insert()
        return config
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear configuración: {str(e)}")


@router.get("/", response_model=PaymentConfigResponse)
async def get_payment_config(
    *,
    current_user: User | Student = Depends(get_current_user)
) -> Any:
    """
    Obtener la configuración de pagos actual
    
    Permisos: Cualquier usuario autenticado (ADMIN o STUDENT)
    
    Los estudiantes necesitan esta información para:
    - Ver el QR de pago
    - Conocer el número de cuenta donde depositar
    - Obtener detalles del banco y titular
    
    Los admins pueden ver además:
    - Quién creó/actualizó la configuración
    - Fechas de creación/actualización
    """
    config = await payment_config_service.get_payment_config()
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="No existe una configuración de pagos. Contacte al administrador."
        )
    
    return config


@router.put("/", response_model=PaymentConfigResponse)
async def update_payment_config(
    *,
    file: Optional[UploadFile] = File(None, description="Nueva imagen del QR (opcional)"),
    numero_cuenta: Optional[str] = Form(None, description="Número de cuenta bancaria"),
    banco: Optional[str] = Form(None, description="Nombre del banco"),
    titular: Optional[str] = Form(None, description="Titular de la cuenta"),
    tipo_cuenta: Optional[str] = Form(None, description="Tipo de cuenta"),
    notas: Optional[str] = Form(None, description="Notas adicionales"),
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Actualizar la configuración de pagos (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    Content-Type: multipart/form-data
    
    Todos los campos son opcionales. Solo se actualizarán los proporcionados.
    
    Permite actualizar:
    - file: Nueva imagen del QR (se sube automáticamente a Cloudinary y reemplaza la anterior)
    - numero_cuenta: Número de cuenta
    - banco, titular, tipo_cuenta: Información bancaria
    - notas: Notas adicionales
    
    Si se proporciona un nuevo QR (file):
    1. Se valida la imagen
    2. Se sube a Cloudinary (reemplaza la imagen anterior)
    3. Se actualiza la URL automáticamente
    
    Casos de uso:
    - Cambio de cuenta bancaria
    - Actualización del QR (por cambio de banco o sistema)
    - Corrección de datos incorrectos
    """
    from core.cloudinary_utils import upload_image
    
    try:
        # Obtener configuración actual
        config = await payment_config_service.get_payment_config()
        if not config:
            raise HTTPException(
                status_code=404,
                detail="No existe una configuración para actualizar. Use POST para crear."
            )
        
        # Si se proporciona nueva imagen, subirla a Cloudinary
        if file:
            folder = "payment_config"
            public_id = "qr_payment"
            qr_url = await upload_image(file, folder, public_id)
            config.qr_url = qr_url
        
        # Actualizar campos si se proporcionaron
        if numero_cuenta is not None:
            config.numero_cuenta = numero_cuenta
        if banco is not None:
            config.banco = banco
        if titular is not None:
            config.titular = titular
        if tipo_cuenta is not None:
            config.tipo_cuenta = tipo_cuenta
        if notas is not None:
            config.notas = notas
        
        # Actualizar auditoría
        config.actualizado_por = current_user.username
        await config.save()
        
        return config
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar configuración: {str(e)}")


@router.delete("/", response_model=PaymentConfigResponse)
async def delete_payment_config(
    *,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Eliminar la configuración de pagos (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    IMPORTANTE: Esta operación NO elimina permanentemente la configuración,
    solo la marca como inactiva.
    
    Esto permite:
    - Mantener un historial de configuraciones
    - Auditoría de cambios
    - Posibilidad de reactivar si fue un error
    
    Después de eliminar, será necesario crear una nueva configuración
    para que los estudiantes puedan realizar pagos.
    
    ADVERTENCIA: Sin una configuración activa, los estudiantes no podrán
    ver el QR ni número de cuenta para realizar pagos.
    """
    config = await payment_config_service.delete_payment_config()
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="No existe una configuración de pagos para eliminar"
        )
    
    return config
