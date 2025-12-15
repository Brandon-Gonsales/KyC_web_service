import asyncio
from core.database import init_db
from models.student import Student
from beanie.operators import RegEx

async def debug_search():
    print("--- Debugging Search ---")
    await init_db()
    
    # 1. Buscar a "Juan Carlos" directamente para ver cómo está guardado
    print("\n1. Buscando 'Juan Carlos' exacto...")
    juan = await Student.find_one(Student.nombre == "Juan Carlos")
    if juan:
        print(f"✅ Encontrado: ID={juan.id}")
        print(f"   Nombre: '{juan.nombre}'")
        print(f"   Email: '{juan.email}'")
        print(f"   Carnet: '{juan.carnet}'")
    else:
        print("❌ No se encontró 'Juan Carlos' exacto. Listando todos los que contienen 'Juan'...")
        candidates = await Student.find(RegEx(Student.nombre, "Juan")).to_list()
        for c in candidates:
             print(f"   - '{c.nombre}'")

    # 2. Probar la Regex que usamos en el servicio
    print("\n2. Probando Regex del servicio: RegEx('.*juan.*', 'i')")
    q = "juan"
    search_regex = RegEx(f"{q}", "i")
    
    results = await Student.find(Student.nombre == search_regex).to_list()
    print(f"Resultados encontrados: {len(results)}")
    for s in results:
        print(f"   - {s.nombre}")

    # 3. Probar directo con PyMongo (bypass Beanie)
    print("\n3. Probando directo con PyMongo...")
    from core.config import settings
    import motor.motor_asyncio
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    cursor = db.students.find({"nombre": {"$regex": "juan", "$options": "i"}})
    docs = await cursor.to_list(length=10)
    print(f"Resultados PyMongo: {len(docs)}")
    for d in docs:
        print(f"   - {d.get('nombre')}")

if __name__ == "__main__":
    asyncio.run(debug_search())
