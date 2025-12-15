import asyncio
from core.database import init_db
from services import student_service
from models.enums import EstadoTitulo

async def test_existing_data():
    print("--- Consultando Datos Existentes ---")
    await init_db()

    # 1. Total de estudiantes
    all_students = await student_service.get_students(limit=1000)
    print(f"\n📊 Total de estudiantes en BD: {len(all_students)}")
    
    # 2. Estudiantes Activos vs Inactivos
    activos = await student_service.get_students(activo=True, limit=1000)
    inactivos = await student_service.get_students(activo=False, limit=1000)
    print(f"✅ Activos: {len(activos)}")
    print(f"✅ Inactivos: {len(inactivos)}")

    # 3. Estados de Títulos
    # Vamos a contar cuántos hay de cada tipo iterando lo que ya trajimos o haciendo queries
    pendientes = await student_service.get_students(estado_titulo=EstadoTitulo.PENDIENTE)
    verificados = await student_service.get_students(estado_titulo=EstadoTitulo.VERIFICADO)
    sin_titulo = await student_service.get_students(estado_titulo=EstadoTitulo.SIN_TITULO)
    
    print(f"\n🎓 Títulos:")
    print(f"   - Pendientes: {len(pendientes)}")
    print(f"   - Verificados: {len(verificados)}")
    print(f"   - Sin Título: {len(sin_titulo)}")
    
    # 4. Muestreo de Cursos
    # Tomamos el primer estudiante que tenga cursos y usamos ese ID para probar el filtro
    student_with_courses = next((s for s in all_students if s.lista_cursos_ids), None)
    
    if student_with_courses:
        course_id = student_with_courses.lista_cursos_ids[0]
        print(f"\n📚 Probando filtro por curso ID: {course_id}")
        in_course = await student_service.get_students(curso_id=course_id)
        print(f"   - Estudiantes encontrados en ese curso: {len(in_course)}")
        for s in in_course:
            print(f"     * {s.nombre}")
    else:
        print("\n⚠️ No se encontraron estudiantes inscritos en cursos para probar el filtro de curso_id.")

if __name__ == "__main__":
    asyncio.run(test_existing_data())
