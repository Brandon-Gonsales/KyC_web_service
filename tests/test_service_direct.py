import asyncio
from core.database import init_db
from services import student_service
from models.enums import EstadoTitulo

async def test_service_filters():
    print("--- Iniciando Pruebas Directas del Servicio de Estudiantes ---")
    
    # 1. Inicializar BD
    print("Conectando a BD...")
    await init_db()
    
    # 2. Test List All
    print("\n1. Obteniendo todos los estudiantes (limit 5)...")
    students = await student_service.get_students(limit=5)
    print(f"✅ Éxito. Se encontraron {len(students)} estudiantes.")
    for s in students:
        print(f"   - {s.nombre} ({s.carnet}) - Activo: {s.activo}")

    # 3. Test Search (q)
    search_term = "juan" 
    print(f"\n2. Buscando por '{search_term}'...")
    students = await student_service.get_students(q=search_term)
    print(f"✅ Encontrados: {len(students)}")
    for s in students:
        print(f"   - {s.nombre} ({s.email})")

    # 4. Test Activo Filter
    print("\n3. Filtrando por Activo=False...")
    students = await student_service.get_students(activo=False)
    print(f"✅ Encontrados inactivos: {len(students)}")

    # 5. Test Estado Titulo
    print("\n4. Filtrando por Título Pendiente...")
    # Nota: Asegurarse de que EstadoTitulo.PENDIENTE coincida con lo que hay en BD
    students = await student_service.get_students(estado_titulo=EstadoTitulo.PENDIENTE)
    print(f"✅ Encontrados con título pendiente: {len(students)}")

if __name__ == "__main__":
    asyncio.run(test_service_filters())
