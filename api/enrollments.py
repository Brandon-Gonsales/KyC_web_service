"""
API de Inscripciones (Enrollments)
==================================

Endpoints para gestionar inscripciones de estudiantes a cursos.

Permisos:
---------
- POST /enrollments/: ADMIN/SUPERADMIN
- GET /enrollments/: ADMIN (todas) / STUDENT (solo las suyas)
- GET /enrollments/{id}: ADMIN / STUDENT (si es suya)
- PATCH /enrollments/{id}: ADMIN/SUPERADMIN
- GET /enrollments/student/{student_id}: ADMIN / STUDENT (si es él mismo)
- GET /enrollments/course/{course_id}: ADMIN
"""

from typing import List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from models.enrollment import Enrollment
from models.student import Student
from models.user import User
from models.enums import EstadoInscripcion
from schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
    EnrollmentWithDetails
)
from services import enrollment_service
from beanie import PydanticObjectId
from api.dependencies import require_admin, get_current_user

router = APIRouter()


@router.post("/", response_model=EnrollmentResponse, status_code=201)
async def create_enrollment(
    *,
    enrollment_in: EnrollmentCreate,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Crear nueva inscripción (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    El sistema calculará automáticamente:
    - Precios según tipo de estudiante (interno/externo)
    - Descuentos (del curso + personalizado)
    - Total a pagar y saldo pendiente
    
    Validaciones:
    - El estudiante existe
    - El curso existe
    - El estudiante no está ya inscrito en ese curso
    """
    try:
        enrollment = await enrollment_service.create_enrollment(
            enrollment_in=enrollment_in,
            admin_username=current_user.username
        )
        return enrollment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


from schemas.common import PaginatedResponse, PaginationMeta
import math

@router.get("/", response_model=PaginatedResponse[EnrollmentResponse])
async def list_enrollments(
    *,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(10, ge=1, le=500, description="Elementos por página"),
    estado: Optional[EstadoInscripcion] = None,
    current_user: User | Student = Depends(get_current_user)
) -> Any:
    """
    Listar inscripciones con paginación
    
    Permisos:
    - ADMIN: Ve todas las inscripciones
    - STUDENT: Ve solo sus propias inscripciones
    
    Filtros disponibles:
    - estado: Filtrar por estado específico
    """
    # Si es admin, retorna todas (paginadas en DB)
    if isinstance(current_user, User):
        enrollments, total_count = await enrollment_service.get_all_enrollments(
            page=page,
            per_page=per_page,
            estado=estado
        )
    
    # Si es estudiante, solo sus inscripciones (paginadas en memoria por ahora)
    elif isinstance(current_user, Student):
        all_enrollments = await enrollment_service.get_enrollments_by_student(
            student_id=current_user.id
        )
        
        # Aplicar filtro de estado si lo pidió
        if estado:
            all_enrollments = [e for e in all_enrollments if e.estado == estado]
            
        total_count = len(all_enrollments)
        
        # Aplicar paginación manual
        start = (page - 1) * per_page
        end = start + per_page
        enrollments = all_enrollments[start:end]
    
    else:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Calcular metadatos comunes
    total_pages = math.ceil(total_count / per_page) if total_count > 0 else 0
    has_next = page < total_pages
    has_prev = page > 1
    
    return {
        "data": enrollments,
        "meta": PaginationMeta(
            page=page,
            limit=per_page,
            totalItems=total_count,
            totalPages=total_pages,
            hasNextPage=has_next,
            hasPrevPage=has_prev
        )
    }


@router.get("/{id}", response_model=EnrollmentResponse)
async def get_enrollment(
    *,
    id: PydanticObjectId,
    current_user: User | Student = Depends(get_current_user)
) -> Any:
    """
    Obtener una inscripción específica
    
    Permisos:
    - ADMIN: Puede ver cualquier inscripción
    - STUDENT: Solo puede ver sus propias inscripciones
    """
    enrollment = await enrollment_service.get_enrollment(id)
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    
    # Si es estudiante, validar que sea suya
    if isinstance(current_user, Student):
        if enrollment.estudiante_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para ver esta inscripción"
            )
    
    return enrollment


@router.patch("/{id}", response_model=EnrollmentResponse)
async def update_enrollment(
    *,
    id: PydanticObjectId,
    enrollment_in: EnrollmentUpdate,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Actualizar una inscripción (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    Permite actualizar:
    - descuento_personalizado: Recalcula automáticamente el total
    - estado: Cambiar el estado manualmente
    """
    try:
        # Actualizar descuento si se proporcionó
        if enrollment_in.descuento_personalizado is not None:
            enrollment = await enrollment_service.update_enrollment_descuento(
                enrollment_id=id,
                descuento_personalizado=enrollment_in.descuento_personalizado,
                admin_username=current_user.username
            )
        
        # Actualizar estado si se proporcionó
        if enrollment_in.estado is not None:
            enrollment = await enrollment_service.cambiar_estado_enrollment(
                enrollment_id=id,
                nuevo_estado=enrollment_in.estado,
                admin_username=current_user.username
            )
        
        # Si no se proporcionó nada, solo retornar la inscripción
        if enrollment_in.descuento_personalizado is None and enrollment_in.estado is None:
            enrollment = await enrollment_service.get_enrollment(id)
            if not enrollment:
                raise HTTPException(status_code=404, detail="Inscripción no encontrada")
        
        return enrollment
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/student/{student_id}", response_model=List[EnrollmentResponse])
async def get_enrollments_by_student(
    *,
    student_id: PydanticObjectId,
    current_user: User | Student = Depends(get_current_user)
) -> Any:
    """
    Obtener todas las inscripciones de un estudiante
    
    Permisos:
    - ADMIN: Puede ver inscripciones de cualquier estudiante
    - STUDENT: Solo puede ver sus propias inscripciones
    """
    # Si es estudiante, validar que pida sus propias inscripciones
    if isinstance(current_user, Student):
        if student_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para ver inscripciones de otros estudiantes"
            )
    
    enrollments = await enrollment_service.get_enrollments_by_student(student_id)
    return enrollments


@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
async def get_enrollments_by_course(
    *,
    course_id: PydanticObjectId,
    current_user: User = Depends(require_admin)
) -> Any:
    """
    Obtener todas las inscripciones de un curso (solo admins)
    
    Requiere: ADMIN o SUPERADMIN
    
    Útil para:
    - Ver lista de estudiantes inscritos
    - Generar reportes de un curso
    - Ver estado de pagos por curso
    """
    enrollments = await enrollment_service.get_enrollments_by_course(course_id)
    return enrollments
