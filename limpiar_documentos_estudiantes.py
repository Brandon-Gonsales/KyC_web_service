"""
Script CORRECTO para Limpiar Documentos de Estudiantes
=======================================================
Usa la misma configuración que el servidor
"""

import asyncio
import sys
import motor.motor_asyncio
from beanie import init_beanie

# Importar la configuración correcta del proyecto
from core.config import settings
from models.student import Student
from models.user import User
from models.course import Course
from models.enrollment import Enrollment
from models.payment import Payment
from models.payment_config import PaymentConfig
from models.discount import Discount


async def verificar_y_limpiar():
    """
    Verifica y limpia los campos de documentos de estudiantes
    """
    print("=" * 70)
    print("🧹 LIMPIAR CAMPOS DE DOCUMENTOS DE ESTUDIANTES")
    print("=" * 70)
    
    # Usar la misma configuración que el servidor
    print(f"\nConexión:")
    print(f"  URL: {settings.MONGODB_URL[:50]}...")
    print(f"  DB: {settings.DATABASE_NAME}")
    
    # Crear cliente usando la configuración del proyecto
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Inicializar Beanie con los mismos modelos
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User,
            Student,
            Course,
            Enrollment,
            Payment,
            PaymentConfig,
            Discount,
        ]
    )
    
    print("✅ Conectado a la base de datos")
    
    # Contar estudiantes
    total = await Student.count()
    print(f"\n📊 Total de estudiantes: {total}")
    
    if total == 0:
        print("\n⚠️  No hay estudiantes en la base de datos")
        client.close()
        return
    
    # Contar cuántos tienen documentos
    con_cv = await Student.find(Student.cv_url != None).count()
    con_ci = await Student.find(Student.ci_url != None).count()
    con_afiliacion = await Student.find(Student.afiliacion_url != None).count()
    con_titulo = await Student.find(Student.titulo != None).count()
    
    print(f"\nEstudiantes con documentos:")
    print(f"  - CV: {con_cv}")
    print(f"  - CI: {con_ci}")
    print(f"  - Afiliación: {con_afiliacion}")
    print(f"  - Título: {con_titulo}")
    
    # Mostrar algunos ejemplos
    print(f"\n📝 Primeros 3 estudiantes:")
    students = await Student.find().limit(3).to_list()
    for i, s in enumerate(students, 1):
        print(f"  {i}. {s.nombre} ({s.registro})")
        docs = []
        if s.cv_url: docs.append("CV")
        if s.ci_url: docs.append("CI")
        if s.afiliacion_url: docs.append("Afiliación")
        if s.titulo: docs.append("Título")
        if docs:
            print(f"     Docs: {', '.join(docs)}")
    
    print(f"\n" + "=" * 70)
    print(f"Se limpiarán los siguientes campos de TODOS los estudiantes:")
    print(f"  - cv_url → null")
    print(f"  - ci_url → null")
    print(f"  - afiliacion_url → null")
    print(f"  - titulo → null")
    print("=" * 70)
    
    confirmacion = input("\n¿Confirmar limpieza? (escribe 'SI' en mayúsculas): ")
    
    if confirmacion == "SI":
        # Actualizar todos los estudiantes
        all_students = await Student.find_all().to_list()
        
        modified_count = 0
        for student in all_students:
            changed = False
            if student.cv_url is not None:
                student.cv_url = None
                changed = True
            if student.ci_url is not None:
                student.ci_url = None
                changed = True
            if student.afiliacion_url is not None:
                student.afiliacion_url = None
                changed = True
            if student.titulo is not None:
                student.titulo = None
                changed = True
            
            if changed:
                await student.save()
                modified_count += 1
        
        print(f"\n✅ {len(all_students)} estudiantes procesados")
        print(f"✅ {modified_count} estudiantes modificados")
        print("\n✅ Todos los campos de documentos limpiados!")
        print("\n💡 Ahora puedes eliminar estos campos del modelo Student:")
        print("   - titulo")
        print("   - ci_url")
        print("   - afiliacion_url")
        print("   - cv_url")
    else:
        print("❌ Operación cancelada (debes escribir 'SI' en mayúsculas)")
    
    client.close()


if __name__ == "__main__":
    try:
        asyncio.run(verificar_y_limpiar())
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
