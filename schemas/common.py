from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationMeta(BaseModel):
    """Metadatos de paginación"""
    page: int = Field(..., description="Número de página actual")
    limit: int = Field(..., description="Elementos por página")
    totalItems: int = Field(..., description="Total de elementos encontrados")
    totalPages: int = Field(..., description="Total de páginas disponibles")
    hasNextPage: bool = Field(..., description="¿Hay página siguiente?")
    hasPrevPage: bool = Field(..., description="¿Hay página anterior?")

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Respuesta genérica paginada.
    
    Estructura:
    {
        "data": [...],
        "meta": { ... }
    }
    """
    data: List[T] = Field(..., description="Lista de resultados")
    meta: PaginationMeta = Field(..., description="Metadatos de paginación")
