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

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from models.student import Student
from schemas.payment_config import (
    PaymentConfigCreate,
    PaymentConfigUpdate,
    PaymentConfigResponse
)
from services import payment_config_service
from api.dependencies import require_admin, get_current_user

router = APIRouter()


@router.post("/", response_model=PaymentConfigResponse, status_code=201)
async def create_payment_config(
    *,
    config_in: PaymentConfigCreate,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Crear la configuración de pagos del sistema (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    IMPORTANTE: Solo puede existir una configuración activa.
    Si ya existe una, se debe actualizar en lugar de crear.
    
    La configuración incluye:
    - Número de cuenta bancaria
    - QR de pago
    - Información adicional (banco, titular, tipo de cuenta)
    
    Esta información será visible para todos los usuarios autenticados
    (admins y estudiantes) al momento de realizar pagos.
    """
    try:
        config = await payment_config_service.create_payment_config(
            config_in=config_in,
            admin_username=current_user.username
        )
        return config
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
    config_in: PaymentConfigUpdate,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Actualizar la configuración de pagos (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    Permite actualizar:
    - Número de cuenta
    - QR de pago (nueva imagen)
    - Banco, titular, tipo de cuenta
    - Notas adicionales
    
    Solo se actualizarán los campos proporcionados.
    Los campos no incluidos en la petición mantendrán su valor actual.
    
    Casos de uso:
    - Cambio de cuenta bancaria
    - Actualización del QR (por cambio de banco o sistema)
    - Corrección de datos incorrectos
    """
    try:
        config = await payment_config_service.update_payment_config(
            config_in=config_in,
            admin_username=current_user.username
        )
        return config
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
