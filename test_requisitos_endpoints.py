# Script de Prueba: Endpoints de Requisitos
# =========================================

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

# ============================================================================
# PASO 1: Login como Estudiante
# ============================================================================

print("=" * 60)
print("PASO 1: Login como Estudiante")
print("=" * 60)

login_data = {
    "registro": "2024001",  # Cambiar por tu registro
    "password": "1234567"   # Cambiar por tu password
}

print(f"\nIntentando login con registro: {login_data['registro']}...")

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        student_token = token_data["access_token"]
        print("✅ Login exitoso!")
        print(f"Token obtenido: {student_token[:30]}...")
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(f"Respuesta: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("\n⚠️ Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    exit(1)

# ============================================================================
# PASO 2: Ver mis Enrollments
# ============================================================================

print("\n" + "=" * 60)
print("PASO 2: Ver mis Enrollments")
print("=" * 60)

headers = {
    "Authorization": f"Bearer {student_token}"
}

try:
    response = requests.get(f"{BASE_URL}/enrollments/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        enrollments = data.get("items", [])
        
        print(f"\n✅ Tienes {len(enrollments)} enrollment(s)")
        
        if enrollments:
            enrollment = enrollments[0]
            enrollment_id = enrollment["_id"]
            print(f"\nUsando enrollment ID: {enrollment_id}")
            print(f"Curso: {enrollment.get('curso_id', 'N/A')}")
        else:
            print("\n❌ No tienes enrollments aún")
            print("⚠️ Pide a un admin que te inscriba en un curso primero")
            exit(1)
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# ============================================================================
# PASO 3: Ver Requisitos del Enrollment
# ============================================================================

print("\n" + "=" * 60)
print("PASO 3: Ver Requisitos")
print("=" * 60)

try:
    response = requests.get(
        f"{BASE_URL}/enrollments/{enrollment_id}/requisitos",
        headers=headers
    )
    
    if response.status_code == 200:
        requisitos_data = response.json()
        
        print(f"\n✅ Requisitos obtenidos:")
        print(f"  Total: {requisitos_data['total']}")
        print(f"  Pendientes: {requisitos_data['pendientes']}")
        print(f"  En proceso: {requisitos_data['en_proceso']}")
        print(f"  Aprobados: {requisitos_data['aprobados']}")
        print(f"  Rechazados: {requisitos_data['rechazados']}")
        
        print("\n📝 Detalles de cada requisito:")
        for idx, req in enumerate(requisitos_data['requisitos']):
            print(f"\n  [{idx}] {req['descripcion']}")
            print(f"      Estado: {req['estado']}")
            print(f"      URL: {req['url'] or 'Sin subir'}")
            if req.get('motivo_rechazo'):
                print(f"      Motivo rechazo: {req['motivo_rechazo']}")
            if req.get('fecha_subida'):
                print(f"      Fecha subida: {req['fecha_subida']}")
        
        # Buscar un requisito pendiente o rechazado para subir
        requisito_index = None
        for idx, req in enumerate(requisitos_data['requisitos']):
            if req['estado'] in ['pendiente', 'rechazado']:
                requisito_index = idx
                break
        
        if requisito_index is not None:
            print(f"\n💡 Puedes subir el requisito [{requisito_index}]")
        else:
            print("\n✅ Todos los requisitos ya están subidos o aprobados")
            
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Respuesta: {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# ============================================================================
# PASO 4: Subir un Requisito (EJEMPLO)
# ============================================================================

print("\n" + "=" * 60)
print("PASO 4: Ejemplo de Cómo Subir un Requisito")
print("=" * 60)

print("""
Para subir un requisito, necesitas un archivo (PDF o imagen).

EJEMPLO CON CURL:
----------------
curl -X PUT http://localhost:8000/api/v1/enrollments/{enrollment_id}/requisitos/{index} \\
  -H "Authorization: Bearer {token}" \\
  -F "file=@C:\\ruta\\al\\documento.pdf"

EJEMPLO CON PYTHON:
------------------
""")

print(f"""
import requests

# Archivo a subir
file_path = "C:\\\\ruta\\\\al\\\\documento.pdf"  # Cambiar ruta

# Index del requisito (ver arriba)
index = {requisito_index if requisito_index is not None else 0}

# Headers
headers = {{
    "Authorization": "Bearer {student_token[:20]}..."
}}

# Subir archivo
with open(file_path, 'rb') as f:
    files = {{'file': f}}
    response = requests.put(
        f"{BASE_URL}/enrollments/{enrollment_id}/requisitos/{{index}}",
        headers=headers,
        files=files
    )

if response.status_code == 200:
    print("✅ Requisito subido exitosamente!")
    print(response.json())
else:
    print(f"❌ Error: {{response.status_code}}")
    print(response.text)
""")

# ============================================================================
# PRUEBA INTERACTIVA (Opcional)
# ============================================================================

print("\n" + "=" * 60)
print("¿Quieres probar subir un requisito ahora?")
print("=" * 60)

if requisito_index is not None:
    print(f"\nRequisito a subir: [{requisito_index}] {requisitos_data['requisitos'][requisito_index]['descripcion']}")
    
    respuesta = input("\n¿Tienes un archivo para probar? (s/n): ").lower()
    
    if respuesta == 's':
        file_path = input("Ruta completa del archivo: ").strip().strip('"')
        
        if Path(file_path).exists():
            print(f"\n📤 Subiendo archivo: {file_path}")
            
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    response = requests.put(
                        f"{BASE_URL}/enrollments/{enrollment_id}/requisitos/{requisito_index}",
                        headers=headers,
                        files=files
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    print("\n✅ ¡Requisito subido exitosamente!")
                    print(f"\nEstado: {result['estado']}")
                    print(f"URL: {result['url']}")
                    print(f"Fecha subida: {result['fecha_subida']}")
                else:
                    print(f"\n❌ Error {response.status_code}")
                    print(response.text)
                    
            except Exception as e:
                print(f"\n❌ Error al subir: {e}")
        else:
            print(f"\n❌ Archivo no encontrado: {file_path}")
    else:
        print("\n👍 OK, puedes usar los ejemplos de arriba cuando tengas un archivo")
else:
    print("\n⚠️ No hay requisitos pendientes para subir en este enrollment")

print("\n" + "=" * 60)
print("FIN DEL SCRIPT")
print("=" * 60)
