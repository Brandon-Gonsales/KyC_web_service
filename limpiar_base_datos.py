"""
Script para Limpiar Base de Datos
==================================

OPCIÓN 1: Eliminar todo EXCEPTO estudiantes
OPCIÓN 2: Mantener estudiantes pero limpiar sus campos de documentos
OPCIÓN 3: Eliminar TODAS las colecciones (reseteo completo)
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "kyc_db")


async def opcion_1_eliminar_todo_excepto_estudiantes():
    """
    Elimina todas las colecciones EXCEPTO students
    Mantiene: students, users (para no perder acceso de admins)
    Elimina: enrollments, payments, courses, discounts, titles, payment_config
    """
    print("=" * 60)
    print("OPCIÓN 1: Eliminar todo excepto estudiantes y usuarios")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    # Colecciones a eliminar
    colecciones_a_eliminar = [
        "enrollments",
        "payments", 
        "courses",
        "discounts",
        "titles",
        "payment_config"
    ]
    
    print("\nColecciones que se eliminarán:")
    for col in colecciones_a_eliminar:
        count = await db[col].count_documents({})
        print(f"  - {col}: {count} documentos")
    
    confirmacion = input("\n¿Estás seguro? (escribe 'SI' para confirmar): ")
    
    if confirmacion == "SI":
        for col in colecciones_a_eliminar:
            result = await db[col].delete_many({})
            print(f"✅ {col}: {result.deleted_count} documentos eliminados")
        print("\n✅ Limpieza completada!")
    else:
        print("❌ Operación cancelada")
    
    client.close()


async def opcion_2_limpiar_campos_documentos():
    """
    Mantiene los estudiantes pero limpia los campos de documentos antiguos
    (cv_url, ci_url, afiliacion_url, titulo)
    """
    print("=" * 60)
    print("OPCIÓN 2: Limpiar campos de documentos de estudiantes")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    # Contar estudiantes
    total = await db.students.count_documents({})
    print(f"\nTotal de estudiantes: {total}")
    
    # Contar cuántos tienen documentos
    con_docs = await db.students.count_documents({
        "$or": [
            {"cv_url": {"$ne": None}},
            {"ci_url": {"$ne": None}},
            {"afiliacion_url": {"$ne": None}},
            {"titulo": {"$ne": None}}
        ]
    })
    print(f"Estudiantes con documentos: {con_docs}")
    
    confirmacion = input("\n¿Limpiar campos de documentos? (escribe 'SI'): ")
    
    if confirmacion == "SI":
        result = await db.students.update_many(
            {},
            {
                "$set": {
                    "cv_url": None,
                    "ci_url": None,
                    "afiliacion_url": None,
                    "titulo": None
                }
            }
        )
        print(f"✅ {result.modified_count} estudiantes actualizados")
        print("✅ Todos los campos de documentos limpiados!")
    else:
        print("❌ Operación cancelada")
    
    client.close()


async def opcion_3_eliminar_todo():
    """
    PELIGRO: Elimina TODAS las colecciones (reseteo completo)
    """
    print("=" * 60)
    print("⚠️  OPCIÓN 3: ELIMINAR TODO (RESETEO COMPLETO)")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    collections = await db.list_collection_names()
    
    print("\nColecciones que se eliminarán:")
    for col in collections:
        count = await db[col].count_documents({})
        print(f"  - {col}: {count} documentos")
    
    print("\n⚠️  ADVERTENCIA: Esto eliminará TODO, incluyendo:")
    print("  - Estudiantes")
    print("  - Usuarios (admins)")
    print("  - Cursos")
    print("  - Enrollments")
    print("  - Pagos")
    print("  - Todo lo demás")
    
    confirmacion = input("\n¿ESTÁS ABSOLUTAMENTE SEGURO? (escribe 'SI ELIMINAR TODO'): ")
    
    if confirmacion == "SI ELIMINAR TODO":
        for col in collections:
            await db[col].drop()
            print(f"✅ {col}: eliminada completamente")
        print("\n✅ Base de datos completamente limpia!")
    else:
        print("❌ Operación cancelada")
    
    client.close()


async def opcion_4_eliminar_enrollments_y_pagos():
    """
    Elimina solo enrollments y payments
    Mantiene: students, users, courses, discounts
    """
    print("=" * 60)
    print("OPCIÓN 4: Eliminar solo enrollments y pagos")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    # Contar
    enrollments_count = await db.enrollments.count_documents({})
    payments_count = await db.payments.count_documents({})
    
    print(f"\nEnrollments: {enrollments_count}")
    print(f"Payments: {payments_count}")
    
    print("\nSe mantendrán:")
    print("  ✅ Students")
    print("  ✅ Users")
    print("  ✅ Courses")
    print("  ✅ Discounts")
    
    confirmacion = input("\n¿Eliminar enrollments y payments? (escribe 'SI'): ")
    
    if confirmacion == "SI":
        # Eliminar enrollments
        result1 = await db.enrollments.delete_many({})
        print(f"✅ Enrollments: {result1.deleted_count} eliminados")
        
        # Eliminar payments
        result2 = await db.payments.delete_many({})
        print(f"✅ Payments: {result2.deleted_count} eliminados")
        
        # Limpiar listas de cursos en students
        result3 = await db.students.update_many(
            {},
            {"$set": {"lista_cursos_ids": []}}
        )
        print(f"✅ Lista de cursos limpiada en {result3.modified_count} estudiantes")
        
        # Limpiar lista de inscritos en courses
        result4 = await db.courses.update_many(
            {},
            {"$set": {"inscritos": []}}
        )
        print(f"✅ Lista de inscritos limpiada en {result4.modified_count} cursos")
        
        print("\n✅ Limpieza completada!")
    else:
        print("❌ Operación cancelada")
    
    client.close()


async def main():
    print("\n" + "=" * 60)
    print("🗑️  SCRIPT DE LIMPIEZA DE BASE DE DATOS")
    print("=" * 60)
    print(f"\nBase de datos: {DB_NAME}")
    print(f"URL: {MONGODB_URL}")
    
    print("\nOpciones disponibles:")
    print("  1. Eliminar todo EXCEPTO estudiantes y usuarios")
    print("  2. Mantener estudiantes pero limpiar campos de documentos")
    print("  3. ⚠️  ELIMINAR TODO (reseteo completo)")
    print("  4. Eliminar solo enrollments y pagos (mantiene students, courses)")
    print("  5. Salir")
    
    opcion = input("\nSelecciona una opción (1-5): ")
    
    if opcion == "1":
        await opcion_1_eliminar_todo_excepto_estudiantes()
    elif opcion == "2":
        await opcion_2_limpiar_campos_documentos()
    elif opcion == "3":
        await opcion_3_eliminar_todo()
    elif opcion == "4":
        await opcion_4_eliminar_enrollments_y_pagos()
    elif opcion == "5":
        print("👋 Saliendo...")
    else:
        print("❌ Opción inválida")


if __name__ == "__main__":
    asyncio.run(main())
