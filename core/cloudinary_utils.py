"""
Utilidades para subir archivos a Cloudinary
============================================

Funciones para subir y gestionar archivos en Cloudinary.
"""

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from core.config import settings
from typing import Optional

# Configurar Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_pdf(
    file: UploadFile,
    folder: str,
    public_id: Optional[str] = None,
    display_name: Optional[str] = None
) -> str:
    """
    Subir un archivo PDF a Cloudinary
    
    Args:
        file: Archivo a subir
        folder: Carpeta en Cloudinary (ej: "students/cv")
        public_id: ID público opcional (nombre del archivo)
        display_name: Nombre para mostrar al descargar (ej: "CV_Juan_Perez.pdf")
        
    Returns:
        URL del archivo subido
        
    Raises:
        HTTPException: Si el archivo no es PDF o hay error al subir
    """
    # Validar que sea PDF
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=400,
            detail=f"El archivo debe ser PDF, recibido: {file.content_type}"
        )
    
    # Validar tamaño (máximo 10MB)
    file.file.seek(0, 2)  # Ir al final del archivo
    file_size = file.file.tell()  # Obtener tamaño
    file.file.seek(0)  # Volver al inicio
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=400,
            detail="El archivo es demasiado grande (máximo 10MB)"
        )
    
    try:
        # Preparar parámetros de subida
        upload_params = {
            "folder": folder,
            "public_id": public_id,
            "resource_type": "raw",  # Para PDFs
            "overwrite": True
        }
        
        # Si se proporciona display_name, agregarlo como contexto
        if display_name:
            upload_params["context"] = f"alt={display_name}"
        
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            **upload_params
        )
        
        # Si hay display_name, modificar la URL para incluir fl_attachment
        url = result["secure_url"]
        if display_name:
            # Insertar fl_attachment con el nombre de descarga
            # URL original: https://res.cloudinary.com/cloud/raw/upload/v123/folder/file.pdf
            # URL modificada: https://res.cloudinary.com/cloud/raw/upload/fl_attachment:nombre/v123/folder/file.pdf
            parts = url.split("/upload/")
            if len(parts) == 2:
                # Limpiar el nombre de archivo (remover caracteres especiales)
                safe_name = display_name.replace(" ", "_").replace("/", "_")
                url = f"{parts[0]}/upload/fl_attachment:{safe_name}/{parts[1]}"
        
        return url
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al subir archivo: {str(e)}"
        )


async def upload_image(
    file: UploadFile,
    folder: str,
    public_id: Optional[str] = None
) -> str:
    """
    Subir una imagen a Cloudinary
    
    Args:
        file: Archivo a subir
        folder: Carpeta en Cloudinary (ej: "students/photos")
        public_id: ID público opcional (nombre del archivo)
        
    Returns:
        URL de la imagen subida
        
    Raises:
        HTTPException: Si el archivo no es imagen o hay error al subir
    """
    # Validar que sea imagen
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo debe ser imagen (JPG, PNG, WEBP), recibido: {file.content_type}"
        )
    
    # Validar tamaño (máximo 5MB)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=400,
            detail="La imagen es demasiado grande (máximo 5MB)"
        )
    
    try:
        # Subir a Cloudinary con transformaciones
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            public_id=public_id,
            resource_type="image",
            overwrite=True,
            transformation=[
                {"width": 800, "height": 800, "crop": "limit"},  # Redimensionar
                {"quality": "auto"},  # Calidad automática
                {"fetch_format": "auto"}  # Formato automático
            ]
        )
        
        return result["secure_url"]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al subir imagen: {str(e)}"
        )


async def delete_file(public_id: str, resource_type: str = "raw") -> bool:
    """
    Eliminar un archivo de Cloudinary
    
    Args:
        public_id: ID público del archivo
        resource_type: Tipo de recurso ("raw" para PDFs, "image" para imágenes)
        
    Returns:
        True si se eliminó correctamente
    """
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return result.get("result") == "ok"
    except Exception:
        return False
