import asyncio
from core.database import init_db
from services import course_service, enrollment_service, payment_service, discount_service, user_service
import math

async def test_all_pagination():
    await init_db()
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write("--- Probando Paginación en TODOS los Servicios ---\n")
        
        # 1. Cursos
        f.write("\n1. Cursos (get_courses)\n")
        courses, total_courses = await course_service.get_courses(page=1, per_page=5)
        f.write(f"   [OK] Items: {len(courses)}, Total: {total_courses}\n")
        
        # 2. Inscripciones
        f.write("\n2. Inscripciones (get_all_enrollments)\n")
        enrollments, total_enrollments = await enrollment_service.get_all_enrollments(page=1, per_page=5)
        f.write(f"   [OK] Items: {len(enrollments)}, Total: {total_enrollments}\n")
        
        # 3. Pagos
        f.write("\n3. Pagos (get_all_payments)\n")
        payments, total_payments = await payment_service.get_all_payments(page=1, per_page=5)
        f.write(f"   [OK] Items: {len(payments)}, Total: {total_payments}\n")
        
        # 4. Descuentos
        f.write("\n4. Descuentos (get_discounts)\n")
        discounts, total_discounts = await discount_service.get_discounts(page=1, per_page=5)
        f.write(f"   [OK] Items: {len(discounts)}, Total: {total_discounts}\n")
        
        # 5. Usuarios
        f.write("\n5. Usuarios (get_users)\n")
        users, total_users = await user_service.get_users(page=1, per_page=5)
        f.write(f"   [OK] Items: {len(users)}, Total: {total_users}\n")

        f.write("\n[SUCCESS] Todas las pruebas de servicio pasaron correctamente.\n")
        print("Reporte generado en final_report.txt")

if __name__ == "__main__":
    asyncio.run(test_all_pagination())
