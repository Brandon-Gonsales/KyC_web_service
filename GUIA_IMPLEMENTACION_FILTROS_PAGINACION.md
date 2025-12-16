# Guía de Implementación: Filtros y Paginación (FastAPI + Svelte)
**Para:** Equipo de Desarrollo (Backend & Frontend)
**Objetivo:** Estandarizar la implementación de listados utilizando FastAPI (Python) y Svelte (JS).

---

## 1. Introducción

Esta guía detalla cómo implementar un sistema de listado eficiente con paginación y filtros de búsqueda. Usaremos como referencia el módulo de **Estudiantes (`Students`)** del proyecto actual.

---

## 2. Backend (FastAPI + Beanie)

### Paso A: El Schema de Respuesta
En lugar de devolver una lista simple, devolvemos un objeto estructurado con metadatos.

**Archivo:** `schemas/common.py` (o definido en cada endpoint)
```python
class PaginatedResponse(BaseModel, Generic[T]):
    total: int          # Total de registros encontrados
    page: int           # Página actual
    per_page: int       # Registros por página
    total_pages: int    # Total de páginas
    data: List[T]       # Lista de objetos
```

### Paso B: El Servicio (Lógica de Negocio)
El servicio debe aceptar parámetros de paginación y filtros opcionales.

**Archivo:** `services/student_service.py`
```python
async def get_students(
    page: int = 1,
    per_page: int = 10,
    q: Optional[str] = None  # Filtro de búsqueda
) -> tuple[List[Student], int]:
    
    query = Student.find()
    
    # 1. Aplicar Filtros (Búsqueda insensible a mayúsculas)
    if q:
        regex = {"$regex": q, "$options": "i"}
        query = query.find(
            Or(
                Student.nombre == regex,
                Student.email == regex,
                Student.carnet == regex
            )
        )
    
    # 2. Obtener Total (CRÍTICO para calcular páginas)
    total_count = await query.count()
    
    # 3. Aplicar Paginación (Skip & Limit)
    skip = (page - 1) * per_page
    students = await query.skip(skip).limit(per_page).to_list()
    
    return students, total_count
```

### Paso C: El Endpoint (Controlador)
El endpoint recibe los Query Params y construye la respuesta paginada.

**Archivo:** `api/students.py`
```python
@router.get("/", response_model=PaginatedResponse[StudentResponse])
async def read_students(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: Optional[str] = None
):
    items, total = await student_service.get_students(page, per_page, q)
    
    # Calcular total de páginas
    total_pages = math.ceil(total / per_page) if per_page > 0 else 0
    
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "data": items
    }
```

### Paso D: Ejemplo de Request y Response

**Request (Lo que envía el Frontend):**
```http
GET /api/v1/students/?page=1&per_page=2&q=juan HTTP/1.1
Host: api.kyc.com
```

**Response (Lo que devuelve el Backend):**
```json
{
  // --- METADATA (Información de Paginación) ---
  "total": 45,            // Hay 45 registros en total en la DB
  "page": 1,              // Página actual
  "per_page": 2,          // Tamaño de página solicitado
  "total_pages": 23,      // Total de páginas disponibles

  // --- DATA (Los registros reales) ---
  "data": [
    {
      "id": "507f1f77bcf86cd799439011",
      "nombre": "Juan Pérez",
      "carnet": "1234567",
      "email": "juan@email.com",
      "activo": true
    },
    {
      "id": "507f1f77bcf86cd799439022",
      "nombre": "Juan Gabriel",
      "carnet": "7654321",
      "email": "juanga@email.com",
      "activo": true
    }
  ]
}
```

---

## 3. Frontend (Svelte)

En Svelte, aprovechamos la reactividad (`$:`) para recargar datos automáticamente cuando cambian los filtros.

### Paso A: Estructura del Componente (`StudentList.svelte`)

```html
<script>
  import { onMount } from 'svelte';
  
  // 1. Estado Local
  let students = [];
  let total = 0;
  let totalPages = 0;
  
  // 2. Parámetros de Filtro (Reactivos)
  let page = 1;
  let perPage = 10;
  let searchQuery = "";
  let loading = false;

  // 3. Función de Carga de Datos
  async def loadStudents() {
    loading = true;
    try {
      // Construir URL con parámetros
      const params = new URLSearchParams({
        page: page.toString(),
        per_page: perPage.toString(),
      });
      
      if (searchQuery) {
        params.append('q', searchQuery);
      }

      const res = await fetch(`/api/v1/students/?${params}`);
      const data = await res.json();

      // Actualizar estado
      students = data.data;
      total = data.total;
      totalPages = data.total_pages;
    } catch (error) {
      console.error("Error cargando estudiantes:", error);
    } finally {
      loading = false;
    }
  }

  // 4. Reactividad: Recargar cuando cambia page o searchQuery
  // Svelte ejecutará esto automáticamente si page o searchQuery cambian
  $: {
    loadStudents(page, searchQuery);
  }

  // 5. Manejo de Búsqueda (Debounce opcional pero recomendado)
  let timer;
  const handleSearch = (e) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      searchQuery = e.target.value;
      page = 1; // Resetear a página 1 al buscar
    }, 300); // Esperar 300ms
  };
</script>

<!-- VISTA -->
<div class="container">
  <!-- Buscador -->
  <input 
    type="text" 
    placeholder="Buscar por nombre, carnet..." 
    on:input={handleSearch}
    class="search-input"
  />

  <!-- Tabla -->
  {#if loading}
    <p>Cargando...</p>
  {:else}
    <table>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Carnet</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        {#each students as student}
          <tr>
            <td>{student.nombre}</td>
            <td>{student.carnet}</td>
            <td>{student.email}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}

  <!-- Paginación -->
  <div class="pagination">
    <button 
      disabled={page === 1} 
      on:click={() => page--}>
      Anterior
    </button>
    
    <span>Página {page} de {totalPages}</span>
    
    <button 
      disabled={page >= totalPages} 
      on:click={() => page++}>
      Siguiente
    </button>
  </div>
</div>

<style>
  .pagination {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    align-items: center;
  }
</style>
```

### Paso B: Claves de la Implementación en Svelte

1.  **Reactividad (`$:`)**: Usamos el bloque reactivo `$: { loadStudents(...) }` para que cualquier cambio en `page` dispare automáticamente una nueva petición. No hace falta llamar a `loadStudents` manualmente en los botones.
2.  **Resetear Página**: Al escribir en el buscador (`handleSearch`), es vital hacer `page = 1`. Si estás en la página 10 y buscas "Juan", es probable que "Juan" solo tenga 1 página de resultados, por lo que la página 10 estaría vacía.
3.  **Debounce**: El `setTimeout` en `handleSearch` evita bombardear al backend con peticiones por cada letra que escribe el usuario.

---

## 4. Resumen de Reglas de Oro

1.  **Backend**: Siempre devuelve `total_pages` y `total`. El frontend los necesita para saber cuándo deshabilitar el botón "Siguiente".
2.  **Frontend**: Usa `URLSearchParams` para construir la query string de forma segura.
3.  **UX**: Muestra un indicador de carga (`loading`) mientras llegan los datos para que el usuario sepa que algo está pasando.
4.  **Svelte**: Aprovecha la sintaxis reactiva `$:`. Es mucho más limpia que usar `useEffect` (React) o watchers manuales.

---
**Fin de la Guía**
