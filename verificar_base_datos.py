"""
Script para Verificar Estado de la Base de Datos
================================================
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "kyc_db")


async def verificar_base_datos():
    """
    Verifica qué hay en la base de datos
    """
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE BASE DE DATOS")
    print("=" * 60)
    
    print(f"\nConexión:")
    print(f"  URL: {MONGODB_URL}")
    print(f"  DB: {DB_NAME}")
    
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DB_NAME]
        
        # Listar todas las colecciones
        collections = await db.list_collection_names()
        
        print(f"\n📂 Colecciones encontradas: {len(collections)}")
        
        if not collections:
            print("\n⚠️  No hay colecciones en la base de datos")
            print("La base de datos está vacía.")
            client.close()
            return
        
        print("\nDetalles por colección:")
        print("-" * 60)
        
        for col_name in sorted(collections):
            count = await db[col_name].count_documents({})
            print(f"  📦 {col_name:20s}: {count:5d} documentos")
        
        print("-" * 60)
        
        # Detalles de students si existe
        if "students" in collections:
            print("\n👥 ESTUDIANTES:")
            total = await db.students.count_documents({})
            
            if total == 0:
                print("  ⚠️  No hay estudiantes en la base de datos")
            else:
                # Ver ejemplos
                students = await db.students.find().limit(3).to_list(length=3)
                
                print(f"  Total: {total}")
                print(f"\n  Primeros 3 estudiantes:")
                for i, s in enumerate(students, 1):
                    print(f"    {i}. {s.get('nombre', 'Sin nombre')} ({s.get('registro', 'Sin registro')})")
                    print(f"       Email: {s.get('email', 'Sin email')}")
                    if s.get('cv_url'):
                        print(f"       ✓ Tiene CV")
                    if s.get('ci_url'):
                        print(f"       ✓ Tiene CI")
                    if s.get('afiliacion_url'):
                        print(f"       ✓ Tiene afiliación")
                    if s.get('titulo'):
                        print(f"       ✓ Tiene título")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error al conectar a la base de datos:")
        print(f"   {str(e)}")
        print(f"\n💡 Verifica que:")
        print(f"   1. MongoDB esté corriendo")
        print(f"   2. La URL sea correcta en el .env: {MONGODB_URL}")
        print(f"   3. El nombre de la BD sea correcto: {DB_NAME}")


if __name__ == "__main__":
    asyncio.run(verificar_base_datos())
