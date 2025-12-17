"""
Schemas de Configuración de Pagos
==================================

Define los schemas Pydantic para operaciones CRUD de la configuración de pagos.

Schemas incluidos:
-----------------
1. PaymentConfigCreate: Para crear la configuración inicial
2. PaymentConfigUpdate: Para actualizar la configuración
3. PaymentConfigResponse: Para mostrar la configuración
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.base import PyObjectId


class PaymentConfigCreate(BaseModel):
    """
    Schema para crear la configuración de pagos
    
    Uso: POST /payment-config/
    
    Solo puede existir una configuración activa a la vez.
    Si ya existe una, se debe actualizar en lugar de crear.
    """
    
    numero_cuenta: str = Field(
        ...,
        min_length=1,
        description="Número de cuenta bancaria"
    )
    
    banco: Optional[str] = Field(
        None,
        description="Nombre del banco"
    )
    
    titular: Optional[str] = Field(
        None,
        description="Nombre del titular de la cuenta"
    )
    
    tipo_cuenta: Optional[str] = Field(
        None,
        description="Tipo de cuenta (Ahorro, Corriente, etc.)"
    )
    
    qr_url: str = Field(
        ...,
        description="URL del QR de pago (imagen en Cloudinary)"
    )
    
    notas: Optional[str] = Field(
        None,
        description="Notas adicionales"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "numero_cuenta": "1234567890",
                "banco": "Banco Nacional de Bolivia",
                "titular": "Universidad Mayor de San Andrés",
                "tipo_cuenta": "Corriente",
                "qr_url": "https://res.cloudinary.com/.../qr_pago.png",
                "notas": "Cuenta oficial para pagos de cursos de posgrado"
            }
        }


class PaymentConfigUpdate(BaseModel):
    """
    Schema para actualizar la configuración de pagos
    
    Uso: PUT /payment-config/
    
    Todos los campos son opcionales.
    Solo se actualizarán los campos proporcionados.
    """
    
    numero_cuenta: Optional[str] = Field(
        None,
        min_length=1,
        description="Número de cuenta bancaria"
    )
    
    banco: Optional[str] = Field(
        None,
        description="Nombre del banco"
    )
    
    titular: Optional[str] = Field(
        None,
        description="Nombre del titular de la cuenta"
    )
    
    tipo_cuenta: Optional[str] = Field(
        None,
        description="Tipo de cuenta"
    )
    
    qr_url: Optional[str] = Field(
        None,
        description="URL del QR de pago"
    )
    
    notas: Optional[str] = Field(
        None,
        description="Notas adicionales"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "numero_cuenta": "9876543210",
                "qr_url": "https://res.cloudinary.com/.../qr_nuevo.png"
            }
        }


class PaymentConfigResponse(BaseModel):
    """
    Schema para mostrar la configuración de pagos
    
    Uso: GET /payment-config/
    
    Este schema se usa tanto para admins como para estudiantes.
    Muestra toda la información necesaria para realizar pagos.
    """
    
    id: PyObjectId = Field(..., alias="_id")
    
    numero_cuenta: str
    banco: Optional[str] = None
    titular: Optional[str] = None
    tipo_cuenta: Optional[str] = None
    
    qr_url: str
    
    is_active: bool
    notas: Optional[str] = None
    
    # Auditoría (solo visible para admins, pero incluido aquí)
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "_id": "507f1f77bcf86cd799439099",
                "numero_cuenta": "1234567890",
                "banco": "Banco Nacional de Bolivia",
                "titular": "Universidad Mayor de San Andrés",
                "tipo_cuenta": "Corriente",
                "qr_url": "https://res.cloudinary.com/.../qr_pago.png",
                "is_active": True,
                "notas": "Cuenta oficial para pagos",
                "creado_por": "admin1",
                "actualizado_por": "admin2",
                "created_at": "2024-12-17T10:00:00",
                "updated_at": "2024-12-17T14:00:00"
            }
        }
    }
