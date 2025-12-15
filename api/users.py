from typing import List, Any
from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from services import user_service
from beanie import PydanticObjectId
from api.dependencies import require_admin, require_superadmin

router = APIRouter()

from schemas.common import PaginatedResponse, PaginationMeta
from fastapi import Query
import math

@router.get("/", response_model=PaginatedResponse[UserResponse])
async def read_users(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Recuperar usuarios con paginación.
    
    Requiere: ADMIN o SUPERADMIN
    """
    users, total_count = await user_service.get_users(page=page, per_page=per_page)
    
    # Calcular metadatos
    total_pages = math.ceil(total_count / per_page)
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        "data": users,
        "meta": PaginationMeta(
            page=page,
            limit=per_page,
            totalItems=total_count,
            totalPages=total_pages,
            hasNextPage=has_next,
            hasPrevPage=has_prev
        )
    }

@router.post("/", response_model=UserResponse)
async def create_user(
    *,
    user_in: UserCreate,
    current_user: User = Depends(require_superadmin)
) -> Any:
    """
    Crear nuevo usuario.
    
    Requiere: SUPERADMIN
    """
    # Verificar que username y email sean únicos
    existing_user = await user_service.get_user_by_username(user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username ya existe")
    
    existing_email = await user_service.get_user_by_email(user_in.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email ya existe")
    
    user = await user_service.create_user(user_in=user_in)
    return user

@router.get("/{id}", response_model=UserResponse)
async def read_user(
    *,
    id: PydanticObjectId,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Obtener usuario por ID.
    
    Requiere: ADMIN o SUPERADMIN
    """
    user = await user_service.get_user(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{id}", response_model=UserResponse)
async def update_user(
    *,
    id: PydanticObjectId,
    user_in: UserUpdate,
    current_user: User = Depends(require_superadmin)
) -> Any:
    """
    Actualizar usuario.
    
    Requiere: SUPERADMIN
    """
    user = await user_service.get_user(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user = await user_service.update_user(user=user, user_in=user_in)
    return user

@router.delete("/{id}", response_model=UserResponse)
async def delete_user(
    *,
    id: PydanticObjectId,
    current_user: User = Depends(require_superadmin)
) -> Any:
    """
    Eliminar usuario.
    
    Requiere: SUPERADMIN
    """
    user = await user_service.get_user(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user = await user_service.delete_user(id=id)
    return user
