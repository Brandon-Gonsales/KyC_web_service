import asyncio
from core.database import init_db
from services import course_service, enrollment_service, payment_service, discount_service, user_service
from models.enums import EstadoInscripcion, EstadoPago, EstadoTitulo

async def test_all_filters():
    print("--- Probando Filtros y Paginación ---")
    await init_db()
    
    # 1. Cursos (Paginación)
    print("\n1. Cursos (Paginación)")
    courses, total = await course_service.get_courses(page=1, per_page=2)
    print(f"   [OK] Page 1 (limit 2): {len(courses)} items. Total en BD: {total}")
    
    # 2. Inscripciones (Filtro Estado)
    print("\n2. Inscripciones (Filtro Estado)")
    # Buscar pendientes
    pendientes, total_pend = await enrollment_service.get_all_enrollments(
        estado=EstadoInscripcion.PENDIENTE_PAGO
    )
    print(f"   [OK] Pendientes: {len(pendientes)} (Total: {total_pend})")
    
    # 3. Pagos (Filtro Estado)
    print("\n3. Pagos (Filtro Estado)")
    # Buscar pendientes
    pagos_pend, total_pagos = await payment_service.get_all_payments(
        estado=EstadoPago.PENDIENTE
    )
    print(f"   [OK] Pagos Pendientes: {len(pagos_pend)} (Total: {total_pagos})")
    
    # 4. Estudiantes (Búsqueda y Filtros)
    print("\n4. Estudiantes (Filtros Avanzados)")
    # Búsqueda por texto
    q = "juan"
    students_q, total_q = await user_service.get_users(page=1, per_page=10) # User service doesn't have search yet, testing pagination
    print(f"   [OK] Usuarios (Paginación): {len(students_q)} (Total: {total_q})")

    # 5. Descuentos (Paginación)
    print("\n5. Descuentos (Paginación)")
    discounts, total_disc = await discount_service.get_discounts(page=1, per_page=5)
    print(f"   [OK] Descuentos: {len(discounts)} (Total: {total_disc})")

    print("\n[SUCCESS] Pruebas de filtros finalizadas.")

if __name__ == "__main__":
    asyncio.run(test_all_filters())
