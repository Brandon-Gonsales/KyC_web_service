"""
Script para Resetear Listas de Cursos de Estudiantes
====================================================
Limpia el campo lista_cursos_ids de todos los estudiantes
"""

import asyncio
import motor.motor_asyncio
from beanie import init_beanie

from core.config import settings
from models.student import Student
from models.user import User
from models.course import Course
from models.enrollment import Enrollment
from models.payment import Payment
from models.payment_config import PaymentConfig
from models.discount import Discount


async def resetear_listas_cursos():
    """
    Resetea lista_cursos_ids de todos los estudiantes a []
    """
    print("=" * 70)
    print("🔄 RESETEAR LISTAS DE CURSOS DE ESTUDIANTES")
    print("=" * 70)
    
    # Conectar
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[User, Student, Course, Enrollment, Payment, PaymentConfig, Discount]
    )
    
    print(f"\n✅ Conectado a: {settings.DATABASE_NAME}")
    
    # Contar estudiantes
    total = await Student.count()
    print(f"📊 Total de estudiantes: {total}")
    
    if total == 0:
        print("\n⚠️  No hay estudiantes")
        client.close()
        return
    
    # Contar cuántos tienen cursos
    con_cursos = await Student.find(Student.lista_cursos_ids != []).count()
    print(f"📚 Estudiantes con cursos: {con_cursos}")
    
    if con_cursos == 0:
        print("\n✅ Todas las listas ya están vacías")
        client.close()
        return
    
    confirmacion = input("\n¿Confirmar reseteo? (escribe 'SI'): ")
    
    if confirmacion == "SI":
        # Resetear todos
        count = 0
        async for student in Student.find_all():
            if student.lista_cursos_ids:
                student.lista_cursos_ids = []
                await student.save()
                count += 1
        
        print(f"\n✅ {count} estudiantes actualizados")
        print("✅ Todas las listas de cursos reseteadas!")
    else:
        print("❌ Operación cancelada")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(resetear_listas_cursos())
