import asyncio
from httpx import AsyncClient
from main import app
from models.user import User
from models.enums import UserRole
from api.dependencies import require_admin
from core.database import init_db
from core.config import settings

# Mock admin user
mock_admin = User(
    username="admin_test",
    email="admin@test.com",
    password="hashed_password",
    rol=UserRole.ADMIN,
    activo=True
)

# Override dependency
async def override_require_admin():
    return mock_admin

app.dependency_overrides[require_admin] = override_require_admin

async def test_filters_async():
    print("--- Iniciando Pruebas de Filtros de Estudiantes (Async) ---")
    
    # 1. Initialize DB manually
    print("Inicializando BD...")
    await init_db()
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        
        # 1. Test List All
        print("\n1. Obteniendo todos los estudiantes (limit 5)...")
        response = await client.get("/api/v1/students/?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito. Se encontraron {len(data)} estudiantes.")
            for s in data:
                print(f"   - {s.get('nombre', 'Sin nombre')} ({s.get('carnet', 'N/A')}) - Activo: {s.get('activo')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")

        # 2. Test Search (q)
        search_term = "juan" 
        print(f"\n2. Buscando por '{search_term}'...")
        response = await client.get(f"/api/v1/students/?q={search_term}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontrados: {len(data)}")
            for s in data:
                print(f"   - {s.get('nombre')} ({s.get('email')})")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")

        # 3. Test Activo Filter
        print("\n3. Filtrando por Activo=False...")
        response = await client.get("/api/v1/students/?activo=false")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontrados inactivos: {len(data)}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")

        # 4. Test Estado Titulo
        print("\n4. Filtrando por Título Pendiente...")
        response = await client.get("/api/v1/students/?estado_titulo=pendiente")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontrados con título pendiente: {len(data)}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Run async main
    asyncio.run(test_filters_async())
