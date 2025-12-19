"""
Schemas de Requisito
===================

Define los schemas Pydantic para operaciones con requisitos.

Schemas incluidos:
-----------------
1. RequisitoTemplateCreate: Para definir requisitos en un curso
2. RequisitoResponse: Para mostrar requisitos en respuestas
3. RequisitoRechazarRequest: Para rechazar un requisito
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.enums import EstadoRequisito


class RequisitoTemplateCreate(BaseModel):
    """
    Schema para crear un template de requisito (en Course)
    
    Uso: POST /courses/ (dentro del body al crear curso)
    """
    
    descripcion: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Descripción del requisito (ej: 'CV actualizado')"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "descripcion": "Curriculum Vitae actualizado (máximo 2 años de antigüedad)"
            }
        }
    }


class RequisitoResponse(BaseModel):
    """
    Schema para mostrar información de un requisito (en Enrollment)
    
    Uso: GET /enrollments/{id}, respuestas de endpoints
    """
    
    descripcion: str
    estado: EstadoRequisito
    url: Optional[str] = None
    motivo_rechazo: Optional[str] = None
    revisado_por: Optional[str] = None
    fecha_subida: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "descripcion": "Curriculum Vitae actualizado",
                "estado": "aprobado",
                "url": "https://res.cloudinary.com/kyc/documentos/cv_maria_lopez.pdf",
                "motivo_rechazo": None,
                "revisado_por": "admin.sistemas",
                "fecha_subida": "2024-12-15T10:30:00"
            }
        }
    }


class RequisitoRechazarRequest(BaseModel):
    """
    Schema para rechazar un requisito
    
    Uso: PUT /enrollments/{id}/requisitos/{index}/rechazar
    """
    
    motivo: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Motivo del rechazo"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "motivo": "La imagen está borrosa y no se puede leer claramente. Por favor, suba un documento escaneado o una fotografía de mejor calidad."
            }
        }
    }


class RequisitoListResponse(BaseModel):
    """
    Schema para listar todos los requisitos de un enrollment
    
    Uso: GET /enrollments/{id}/requisitos
    """
    
    total: int = Field(
        ...,
        description="Cantidad total de requisitos"
    )
    
    pendientes: int = Field(
        ...,
        description="Cantidad de requisitos pendientes (no subidos)"
    )
    
    en_proceso: int = Field(
        ...,
        description="Cantidad de requisitos en proceso (subidos, esperando revisión)"
    )
    
    aprobados: int = Field(
        ...,
        description="Cantidad de requisitos aprobados"
    )
    
    rechazados: int = Field(
        ...,
        description="Cantidad de requisitos rechazados"
    )
    
    requisitos: list[RequisitoResponse] = Field(
        ...,
        description="Lista completa de requisitos"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 3,
                "pendientes": 1,
                "en_proceso": 1,
                "aprobados": 1,
                "rechazados": 0,
                "requisitos": [
                    {
                        "descripcion": "Curriculum Vitae actualizado",
                        "estado": "aprobado",
                        "url": "https://res.cloudinary.com/kyc/cv_maria.pdf",
                        "motivo_rechazo": None,
                        "revisado_por": "admin.sistemas",
                        "fecha_subida": "2024-12-15T10:30:00"
                    },
                    {
                        "descripcion": "Fotocopia de Cédula de Identidad (ambos lados)",
                        "estado": "en_proceso",
                        "url": "https://res.cloudinary.com/kyc/ci_maria.pdf",
                        "motivo_rechazo": None,
                        "revisado_por": None,
                        "fecha_subida": "2024-12-16T11:00:00"
                    },
                    {
                        "descripcion": "Título profesional en provisión nacional",
                        "estado": "pendiente",
                        "url": None,
                        "motivo_rechazo": None,
                        "revisado_por": None,
                        "fecha_subida": None
                    }
                ]
            }
        }
    }
