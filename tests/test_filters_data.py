import asyncio
from core.database import init_db
from services import student_service
from models.student import Student
from models.title import Title
from models.enums import EstadoTitulo, TipoEstudiante
from beanie import PydanticObjectId

async def test_other_filters():
    print("--- Probando Filtros Avanzados (Creando datos de prueba) ---")
    await init_db()

    # 1. Crear Estudiante INACTIVO
    print("\nCreating inactive student...")
    inactive_student = Student(
        registro="TEST_INACTIVE",
        password="hash",
        nombre="Test Inactivo",
        activo=False,
        email="inactive@test.com"
    )
    await inactive_student.insert()
    
    # 2. Crear Estudiante con Título PENDIENTE
    print("Creating student with pending title...")
    pending_title_student = Student(
        registro="TEST_PENDING",
        password="hash",
        nombre="Test Titulo Pendiente",
        activo=True,
        email="pending@test.com",
        titulo=Title(
            titulo="Ingeniero de Prueba",
            numero_titulo="123",
            año_expedicion="2023",
            universidad="U Test",
            titulo_url="http://url.com",
            estado=EstadoTitulo.PENDIENTE
        )
    )
    await pending_title_student.insert()

    # 3. Crear Estudiante en un Curso Ficticio
    fake_course_id = PydanticObjectId()
    print(f"Creating student in course {fake_course_id}...")
    course_student = Student(
        registro="TEST_COURSE",
        password="hash",
        nombre="Test Curso",
        activo=True,
        email="course@test.com",
        lista_cursos_ids=[fake_course_id]
    )
    await course_student.insert()

    try:
        # --- PROBAR FILTROS ---
        
        # Test Activo=False
        print("\n--- Probando Filtro: ACTIVO=False ---")
        results = await student_service.get_students(activo=False)
        found = any(s.registro == "TEST_INACTIVE" for s in results)
        print(f"✅ Encontrado 'Test Inactivo': {found}")
        print(f"   Total inactivos: {len(results)}")

        # Test Estado Titulo=PENDIENTE
        print("\n--- Probando Filtro: TITULO=PENDIENTE ---")
        results = await student_service.get_students(estado_titulo=EstadoTitulo.PENDIENTE)
        found = any(s.registro == "TEST_PENDING" for s in results)
        print(f"✅ Encontrado 'Test Titulo Pendiente': {found}")
        print(f"   Total pendientes: {len(results)}")

        # Test Curso ID
        print(f"\n--- Probando Filtro: CURSO_ID={fake_course_id} ---")
        results = await student_service.get_students(curso_id=fake_course_id)
        found = any(s.registro == "TEST_COURSE" for s in results)
        print(f"✅ Encontrado 'Test Curso': {found}")
        print(f"   Total en curso: {len(results)}")

    finally:
        # Cleanup
        print("\n--- Limpiando datos de prueba ---")
        await inactive_student.delete()
        await pending_title_student.delete()
        await course_student.delete()
        print("Datos eliminados.")

if __name__ == "__main__":
    asyncio.run(test_other_filters())
