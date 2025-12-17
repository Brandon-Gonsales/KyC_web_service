"""
Servicio de Configuración de Pagos
===================================

Lógica de negocio para operaciones CRUD de la configuración de pagos.

IMPORTANTE: Este es un patrón SINGLETON, solo puede existir una configuración activa.
"""

from typing import Optional
from models.payment_config import PaymentConfig
from schemas.payment_config import PaymentConfigCreate, PaymentConfigUpdate


async def get_payment_config() -> Optional[PaymentConfig]:
    """
    Obtener la configuración de pagos activa
    
    Returns:
        PaymentConfig: La configuración activa, o None si no existe
    """
    return await PaymentConfig.find_one(PaymentConfig.is_active == True)


async def create_payment_config(
    config_in: PaymentConfigCreate,
    admin_username: str
) -> PaymentConfig:
    """
    Crear la configuración de pagos
    
    IMPORTANTE: Si ya existe una configuración activa, lanzará un error.
    Solo puede existir una configuración activa a la vez.
    
    Args:
        config_in: Datos de la configuración a crear
        admin_username: Username del admin que crea la configuración
        
    Returns:
        PaymentConfig: La configuración creada
        
    Raises:
        ValueError: Si ya existe una configuración activa
    """
    # Verificar que no exista ya una configuración activa
    existing = await get_payment_config()
    if existing:
        raise ValueError(
            "Ya existe una configuración de pagos activa. "
            "Debe actualizar la existente o eliminarla primero."
        )
    
    # Crear nueva configuración
    config = PaymentConfig(
        **config_in.model_dump(),
        creado_por=admin_username,
        actualizado_por=admin_username,
        is_active=True
    )
    await config.insert()
    return config


async def update_payment_config(
    config_in: PaymentConfigUpdate,
    admin_username: str
) -> PaymentConfig:
    """
    Actualizar la configuración de pagos activa
    
    Args:
        config_in: Datos a actualizar (solo campos proporcionados)
        admin_username: Username del admin que actualiza
        
    Returns:
        PaymentConfig: La configuración actualizada
        
    Raises:
        ValueError: Si no existe una configuración activa
    """
    config = await get_payment_config()
    if not config:
        raise ValueError(
            "No existe una configuración de pagos. "
            "Debe crear una primero."
        )
    
    # Actualizar solo los campos proporcionados
    update_data = config_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(config, field, value)
    
    config.actualizado_por = admin_username
    await config.save()
    return config


async def delete_payment_config() -> PaymentConfig:
    """
    Eliminar la configuración de pagos activa
    
    Returns:
        PaymentConfig: La configuración eliminada, o None si no existía
        
    Nota:
        Esto marcará la configuración como inactiva en lugar de eliminarla.
        Así se mantiene un historial.
    """
    config = await get_payment_config()
    if config:
        config.is_active = False
        await config.save()
    return config


async def delete_payment_config_permanently() -> Optional[PaymentConfig]:
    """
    Eliminar PERMANENTEMENTE la configuración de pagos
    
    ADVERTENCIA: Esta acción es irreversible.
    Se recomienda usar delete_payment_config() en su lugar.
    
    Returns:
        PaymentConfig: La configuración eliminada, o None si no existía
    """
    config = await get_payment_config()
    if config:
        await config.delete()
    return config
