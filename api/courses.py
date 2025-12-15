from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from models.course import Course
from models.user import User
from models.student import Student
from schemas.course import CourseCreate, CourseResponse, CourseUpdate, CourseEnrolledStudent
from services import course_service
from beanie import PydanticObjectId
from api.dependencies import require_admin, require_superadmin, get_current_user

router = APIRouter()

from schemas.common import PaginatedResponse, PaginationMeta
from fastapi import Query
import math

@router.get("/", response_model=PaginatedResponse[CourseResponse])
async def read_courses(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=100, description="Elementos por página"),
    current_user: Union[User, Student] = Depends(get_current_user)
) -> Any:
    """
    Recuperar cursos con paginación.
    
    Requiere: Autenticación (cualquier rol)
    """
    courses, total_count = await course_service.get_courses(page=page, per_page=per_page)
    
    # Calcular metadatos
    total_pages = math.ceil(total_count / per_page)
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        "data": courses,
        "meta": PaginationMeta(
            page=page,
            limit=per_page,
            totalItems=total_count,
            totalPages=total_pages,
            hasNextPage=has_next,
            hasPrevPage=has_prev
        )
    }

@router.post("/", response_model=CourseResponse)
async def create_course(
    *,
    course_in: CourseCreate,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Crear nuevo curso.
    
    Requiere: ADMIN o SUPERADMIN
    """
    course = await course_service.create_course(course_in=course_in)
    return course

@router.get("/{id}", response_model=CourseResponse)
async def read_course(
    *,
    id: PydanticObjectId,
    current_user: Union[User, Student] = Depends(get_current_user)
) -> Any:
    """
    Obtener curso por ID.
    
    Requiere: Autenticación (cualquier rol)
    """
    course = await course_service.get_course(id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course

@router.put("/{id}", response_model=CourseResponse)
async def update_course(
    *,
    id: PydanticObjectId,
    course_in: CourseUpdate,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Actualizar curso.
    
    Requiere: ADMIN o SUPERADMIN
    """
    course = await course_service.get_course(id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    course = await course_service.update_course(course=course, course_in=course_in)
    return course

@router.delete("/{id}", response_model=CourseResponse)
async def delete_course(
    *,
    id: PydanticObjectId,
    current_user: User = Depends(require_superadmin)
) -> Any:
    """
    Eliminar curso.
    
    Requiere: SUPERADMIN
    """
    course = await course_service.get_course(id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    course = await course_service.delete_course(id=id)
    return course

@router.get("/{id}/students", response_model=List[CourseEnrolledStudent])
async def get_course_students(
    *,
    id: PydanticObjectId,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Obtener reporte detallado de estudiantes inscritos en un curso.
    
    Requiere: ADMIN o SUPERADMIN
    
    Retorna una lista con:
    - Datos personales del estudiante (nombre, carnet, contacto)
    - Datos de inscripción (fecha, estado, tipo)
    - Datos financieros (total a pagar, pagado, saldo, % avance)
    """
    # Verificar que el curso existe
    course = await course_service.get_course(id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    report = await course_service.get_course_students(course_id=id)
    return report
