# Implementación Simple Docker - TODO App

Una aplicación de tareas (TODO) implementada con Docker que incluye una arquitectura de base de datos primaria-replica para demostrar conceptos de replicación y contenedorización.

## 📋 Descripción

Este proyecto es una implementación simple de una aplicación TODO que utiliza Docker para orquestar múltiples servicios:

- **Frontend**: Interfaz de usuario para gestionar tareas
- **Backend**: API REST para operaciones CRUD
- **Base de datos primaria**: Servidor de base de datos principal
- **Base de datos réplica**: Servidor de base de datos de solo lectura para distribución de carga

## 🏗️ Arquitectura

```
┌─────────────┐
│   Frontend  │
│  (HTML/CSS) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │
│   (Python)  │
└──────┬──────┘
       │
       ├──────────┐
       ▼          ▼
┌──────────┐  ┌──────────┐
│ DB       │  │ DB       │
│ Primaria │──▶ Réplica  │
└──────────┘  └──────────┘
```

## 🚀 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Windows

- [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux)
- [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/) (versión 4.0 o superior)
- [Python 3.8+](https://www.python.org/downloads/) instalado en WSL

### Linux

- [Docker](https://docs.docker.com/engine/install/) (versión 20.10 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versión 2.0 o superior)
- [Python 3.8+](https://www.python.org/downloads/)

### macOS

- [Docker Desktop para Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Python 3.8+](https://www.python.org/downloads/)

### Verificar instalación

```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Python
python --version
# o
python3 --version

# Para usuarios de Windows, verificar WSL
wsl --list --verbose
```

## 📦 Instalación

### 1. Configuración inicial (Windows)

Si estás en Windows, primero configura WSL:

```bash
# Instalar WSL 2
wsl --install

# Establecer WSL 2 como versión predeterminada
wsl --set-default-version 2

# Instalar una distribución de Linux (Ubuntu recomendado)
wsl --install -d Ubuntu

# Verificar instalación
wsl --list --verbose
```

Inicia Docker Desktop y asegúrate de que la integración con WSL esté habilitada en: **Settings > Resources > WSL Integration**

### 2. Clonar el repositorio

```bash
# En WSL (Windows) o terminal (Linux/macOS)
git clone https://github.com/JuliiizLargo/Implementacion-simple-docker.git
cd Implementacion-simple-docker
```

### 3. Verificar Python

```bash
# Verificar que Python está instalado
python3 --version

# Si no está instalado (en Ubuntu/WSL):
sudo apt update
sudo apt install python3 python3-pip
```

### 4. Construir y levantar los contenedores

```bash
docker-compose up --build
```

O en modo detached (segundo plano):

```bash
docker-compose up -d --build
```

### 5. Acceder a la aplicación

Una vez que los contenedores estén corriendo, abre tu navegador en:

```
http://localhost:8081
```

## 🛠️ Comandos Útiles

### Iniciar los servicios

```bash
docker-compose up
```

### Detener los servicios

```bash
docker-compose down
```

### Ver logs en tiempo real

```bash
docker-compose logs -f
```

### Ver logs de un servicio específico

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reconstruir las imágenes

```bash
docker-compose build --no-cache
```

### Listar contenedores activos

```bash
docker-compose ps
```

### Ejecutar comandos en un contenedor

```bash
docker-compose exec backend bash
```

### Eliminar volúmenes y contenedores

```bash
docker-compose down -v
```

## 📁 Estructura del Proyecto

```
Implementacion-simple-docker/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── estilos.css
│   └── tareas.html
├── docker-compose.yml
└── README.md
```

## 🔧 Configuración

### Variables de Entorno

Las configuraciones principales se encuentran en el archivo `docker-compose.yml`. Puedes modificar:

- Puertos de exposición
- Credenciales de base de datos
- Configuración de replicación

### Base de Datos

La aplicación implementa una arquitectura master-replica:

- **Base de datos primaria**: Maneja operaciones de escritura
- **Base de datos réplica**: Maneja operaciones de lectura para distribución de carga

## 🧪 Desarrollo

### Modificar el código

Los cambios en el código fuente requieren reconstruir los contenedores:

```bash
docker-compose down
docker-compose up --build
```

### Debugging

Para ver información detallada de los contenedores:

```bash
docker-compose logs --tail=100 backend
docker inspect <container_id>
```

## 📊 Monitoreo

### Ver estado de los servicios

```bash
docker-compose ps
```

### Verificar uso de recursos

```bash
docker stats
```

## 🔒 Seguridad

⚠️ **Advertencia**: Esta es una implementación de desarrollo. Para producción:

- Cambiar credenciales por defecto
- Implementar HTTPS
- Configurar firewalls y reglas de red
- Usar secrets de Docker para información sensible
- Actualizar dependencias regularmente

## 🐛 Solución de Problemas

### Los contenedores no inician

```bash
# Ver logs detallados
docker-compose logs

# Verificar que los puertos no estén en uso
netstat -an | grep <puerto>
```

### Error de conexión a base de datos

```bash
# Verificar que el contenedor de la BD esté corriendo
docker-compose ps

# Reiniciar los servicios
docker-compose restart
```

### Problemas con volúmenes

```bash
# Eliminar volúmenes y empezar limpio
docker-compose down -v
docker-compose up --build
```

### Docker Desktop no inicia (Windows)

```bash
# Verificar que la virtualización está habilitada en BIOS
# Verificar que WSL 2 está instalado correctamente
wsl --list --verbose

# Reiniciar el servicio de Docker
# En PowerShell como administrador:
Restart-Service docker
```

### WSL no encuentra Docker

```bash
# Asegúrate de que Docker Desktop está corriendo
# Verifica la integración WSL en Docker Desktop:
# Settings > Resources > WSL Integration > Habilita tu distribución

# Reinicia WSL
wsl --shutdown
wsl
```

### Python no encontrado en WSL

```bash
# Instalar Python en Ubuntu/WSL
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verificar instalación
python3 --version
pip3 --version
```

### Error de permisos en Docker (Linux)

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a iniciar
# O ejecutar:
newgrp docker
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## ✨ Características

- ✅ Arquitectura de microservicios con Docker
- ✅ Replicación de base de datos
- ✅ Frontend responsivo
- ✅ API RESTful
- ✅ Fácil de desplegar y escalar

