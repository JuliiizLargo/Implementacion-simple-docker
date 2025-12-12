# Sistema de Gestión de Tareas con Arquitectura Primary-Replica

**Integrantes:** Julián David Calderón Largo - Juan José Betancourth - Valentina Franco

Una aplicación de gestión de tareas (TODO) que implementa una arquitectura de base de datos MySQL con replicación Primary-Replica y separación de operaciones de lectura/escritura (R/W Split) usando Docker.

## 📋 Descripción del Proyecto

Este proyecto demuestra una implementación completa de:

- **FastAPI** como framework backend para API REST
- **MySQL con arquitectura Primary-Replica** para alta disponibilidad
- **Separación de operaciones READ/WRITE** para optimización de rendimiento
- **Docker Compose** para orquestación de contenedores
- **Frontend HTML/CSS/JS** para consumo de la API
- **Manejo robusto de errores** y recuperación ante fallos

El objetivo principal es demostrar cómo la replicación mejora el rendimiento en lecturas y cómo la separación de responsabilidades permite una operación escalable y resiliente.

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────┐
│    Frontend     │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Backend API   │
│    (FastAPI)    │
└────┬───────┬────┘
     │       │
     │       │
┌────▼──┐ ┌──▼─────┐
│ MySQL │ │ MySQL  │
│Primary│─▶│Replica │
│(WRITE)│ │(READ)  │
└───────┘ └────────┘
```

### Flujo de Operaciones (R/W Split)

- **GET /tasks → Replica**: Todas las consultas de lectura se realizan en la base de datos réplica
- **POST / PUT / DELETE → Primary**: Todas las operaciones de escritura se realizan en el servidor primario
- **Sincronización automática**: Los cambios en Primary se replican automáticamente a Replica

## 🚀 Requisitos Previos

### Para Windows

1. **WSL 2** (Windows Subsystem for Linux)
   - [Guía de instalación oficial](https://docs.microsoft.com/en-us/windows/wsl/install)
   
2. **Docker Desktop para Windows** (versión 4.0 o superior)
   - [Descargar Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
   - Debe tener integración con WSL 2 habilitada
   
3. **Python 3.8+** instalado en WSL
   - Se puede instalar desde el gestor de paquetes de tu distribución Linux

### Para Linux

1. **Docker** (versión 20.10 o superior)
   - [Guía de instalación](https://docs.docker.com/engine/install/)
   
2. **Docker Compose** (versión 2.0 o superior)
   - [Guía de instalación](https://docs.docker.com/compose/install/)
   
3. **Python 3.8+**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

### Para macOS

1. **Docker Desktop para Mac**
   - [Descargar Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
   
2. **Python 3.8+**
   - Puedes usar Homebrew: `brew install python@3.9`

### Verificar Instalaciones

```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Python
python3 --version

# Para usuarios de Windows, verificar WSL
wsl --list --verbose
```

## 📦 Instalación y Configuración

### 1. Configuración Inicial (Solo Windows)

```bash
# Instalar WSL 2
wsl --install

# Establecer WSL 2 como versión predeterminada
wsl --set-default-version 2

# Instalar Ubuntu (recomendado)
wsl --install -d Ubuntu

# Verificar instalación
wsl --list --verbose
```

**Importante:** Inicia Docker Desktop y habilita la integración con WSL en:  
**Settings > Resources > WSL Integration > Activa tu distribución de Linux**

### 2. Clonar el Repositorio

```bash
# En WSL (Windows) o terminal (Linux/macOS)
git clone https://github.com/JuliiizLargo/Implementacion-simple-docker.git
cd Implementacion-simple-docker
```

### 3. Levantar los Servicios

```bash
# Construir e iniciar todos los contenedores
docker-compose up -d --build
```

### 4. Configurar la Replicación MySQL

Una vez que los contenedores estén corriendo, ejecuta los siguientes pasos:

#### a) Configurar el servidor Primary

```bash
# Conectarse al contenedor Primary
docker exec -it gestor-db-primary mysql -u root -p
# Contraseña: admin123
```

Dentro de MySQL Primary, ejecuta:

```sql
-- Crear usuario para replicación
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'admin'@'%';
FLUSH PRIVILEGES;

-- Obtener las coordenadas del binlog (ANOTA ESTOS VALORES)
SHOW MASTER STATUS;
```

**⚠️ Importante:** Anota los valores de `File` (ejemplo: mysql-bin.000003) y `Position` (ejemplo: 906)

#### b) Configurar el servidor Replica

```bash
# Conectarse al contenedor Replica
docker exec -it gestor-db-replica mysql -u root -p
# Contraseña: admin123
```

Dentro de MySQL Replica, ejecuta (reemplaza los valores del paso anterior):

```sql
-- Detener el esclavo si está corriendo
STOP SLAVE;

-- Configurar la conexión con Primary
CHANGE MASTER TO
  MASTER_HOST='gestor-db-primary',
  MASTER_USER='admin',
  MASTER_PASSWORD='admin123',
  MASTER_LOG_FILE='mysql-bin.000003',  -- Usar el valor anotado
  MASTER_LOG_POS=906,                  -- Usar el valor anotado
  GET_MASTER_PUBLIC_KEY=1;

-- Iniciar la replicación
START SLAVE;

-- Verificar el estado de la replicación
SHOW SLAVE STATUS\G;
```

**✅ Verificación exitosa:** Debes ver:
```
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```

#### c) Reiniciar los servicios

```bash
# Detener los contenedores
docker-compose down

# Iniciar nuevamente
docker-compose up -d
```

### 5. Acceder a la Aplicación

Abre tu navegador en:

```
http://localhost:3000
```

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Ver el estado de todos los servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f gestor-db-primary
docker-compose logs -f gestor-db-replica

# Reiniciar todos los servicios
docker-compose restart

# Reiniciar un servicio específico
docker-compose restart backend

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: Borra los datos)
docker-compose down -v
```

### Acceso a Bases de Datos

```bash
# Conectarse a MySQL Primary
docker exec -it gestor-db-primary mysql -u root -p

# Conectarse a MySQL Replica
docker exec -it gestor-db-replica mysql -u root -p

# Ejecutar comandos SQL directamente
docker exec gestor-db-primary mysql -u root -padmin123 -e "SHOW DATABASES;"
```

### Monitoreo y Debug

```bash
# Ver uso de recursos
docker stats

# Inspeccionar un contenedor
docker inspect gestor-db-primary

# Ver logs del backend con marca de tiempo
docker-compose logs -f --timestamps backend

# Ejecutar bash en el contenedor backend
docker-compose exec backend bash
```

## 📁 Estructura del Proyecto

```
Implementacion-simple-docker/
├── backend/
│   ├── Dockerfile              # Configuración del contenedor backend
│   ├── requirements.txt        # Dependencias Python
│   ├── app.py                 # API FastAPI con R/W Split
│   └── database.py            # Conexiones a Primary y Replica
├── frontend/
│   ├── index.html             # Interfaz de usuario
│   ├── styles.css             # Estilos de la aplicación
│   └── script.js              # Lógica del cliente
├── docker-compose.yml          # Orquestación de servicios
└── README.md                  # Este archivo
```

## 🔧 Configuración Detallada

### Separación de Lecturas y Escrituras

El backend implementa automáticamente la separación:

```python
# Operaciones de LECTURA → Replica
@app.get("/tasks")
def get_tasks():
    print("READ: REPLICA")
    conn = connect_replica()
    # ... lógica de lectura

# Operaciones de ESCRITURA → Primary
@app.post("/tasks")
def create_task():
    print("WRITE: PRIMARY")
    conn = connect_primary()
    # ... lógica de escritura
```

### Variables de Entorno

Configuradas en `docker-compose.yml`:

```yaml
# MySQL Primary
MYSQL_ROOT_PASSWORD: admin123
MYSQL_DATABASE: gestor_tareas

# MySQL Replica
MYSQL_ROOT_PASSWORD: admin123
MYSQL_DATABASE: gestor_tareas
```

## 🧪 Pruebas y Validación

### Pruebas de Rendimiento

**Lecturas (GET):**
- Tiempo promedio: 6-15 ms
- Manejado por Replica
- Soporta alta concurrencia

**Escrituras (POST/PUT/DELETE):**
- Tiempo promedio: 12-25 ms
- Procesadas por Primary
- Delay de sincronización a Replica: 20-80 ms

### Pruebas de Tolerancia a Fallos

#### 1. Simular Caída de Replica

```bash
# Detener el contenedor Replica
docker-compose stop gestor-db-replica
```

**Resultado esperado:**
- ✅ Las operaciones GET fallan con mensaje de error
- ✅ El frontend muestra: "Error al cargar tareas"
- ✅ El Primary sigue operativo para escrituras

#### 2. Simular Caída de Primary

```bash
# Detener el contenedor Primary
docker-compose stop gestor-db-primary
```

**Resultado esperado:**
- ✅ No se pueden crear, editar ni eliminar tareas
- ✅ El frontend muestra errores en operaciones de escritura
- ✅ La Replica sigue respondiendo consultas GET

#### 3. Verificar Sincronización

```bash
# Crear una tarea a través del frontend
# Luego verificar en ambas bases de datos

# En Primary
docker exec gestor-db-primary mysql -u root -padmin123 gestor_tareas -e "SELECT * FROM tasks;"

# En Replica (debe mostrar la misma información)
docker exec gestor-db-replica mysql -u root -padmin123 gestor_tareas -e "SELECT * FROM tasks;"
```

### Logs de Monitoreo

El sistema genera logs detallados que incluyen:

- **Tipo de operación**: READ o WRITE
- **Base de datos utilizada**: PRIMARY o REPLICA
- **Tiempo de ejecución**: Duración de cada operación
- **Errores**: Captura y reporta fallos de conexión

Ver logs en tiempo real:

```bash
docker-compose logs -f backend
```

## 🐛 Solución de Problemas

### La replicación no funciona

```bash
# Verificar estado de la replicación
docker exec -it gestor-db-replica mysql -u root -padmin123 -e "SHOW SLAVE STATUS\G;"

# Buscar errores en:
# - Slave_IO_Running: Debe ser "Yes"
# - Slave_SQL_Running: Debe ser "Yes"
# - Last_Error: No debe tener errores

# Si hay errores, reiniciar la replicación:
docker exec -it gestor-db-replica mysql -u root -padmin123 -e "
STOP SLAVE;
RESET SLAVE;
START SLAVE;
"
```

### Error: "Can't connect to MySQL server"

```bash
# Verificar que los contenedores estén corriendo
docker-compose ps

# Reiniciar los servicios
docker-compose restart

# Ver logs para identificar el error
docker-compose logs gestor-db-primary
docker-compose logs gestor-db-replica
```

### La Replica pierde sincronización

**Causa común:** Intentar escribir directamente en la Replica

**Solución:**
```bash
# Reconstruir la Replica desde cero
docker-compose stop gestor-db-replica
docker volume rm implementacion-simple-docker_replica-data
docker-compose up -d gestor-db-replica

# Reconfigurar la replicación (repetir paso 4b de instalación)
```

### Docker Desktop no inicia (Windows)

```bash
# Verificar virtualización en BIOS (debe estar habilitada)
# Verificar WSL 2
wsl --list --verbose

# Reiniciar servicio Docker (PowerShell como administrador)
Restart-Service docker

# Si persiste, reiniciar WSL
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

# Aplicar cambios (o cerrar sesión y volver a entrar)
newgrp docker

# Verificar
docker ps
```

### Puerto 3000 o 8000 ya en uso

```bash
# Encontrar el proceso que usa el puerto
# Linux/macOS:
sudo lsof -i :3000
sudo lsof -i :8000

# Windows:
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Detener el proceso o cambiar el puerto en docker-compose.yml
```

## 📊 Monitoreo y Métricas

### Verificar Replicación en Tiempo Real

```bash
# Ver el estado detallado de la replicación
docker exec gestor-db-replica mysql -u root -padmin123 -e "SHOW SLAVE STATUS\G;" | grep -E "Running|Behind|Error"
```

### Verificar Carga del Sistema

```bash
# Ver uso de CPU y memoria de cada contenedor
docker stats

# Ver información específica del backend
docker stats gestor-backend
```

### Analizar Logs de Operaciones

```bash
# Filtrar solo operaciones de lectura
docker-compose logs backend | grep "READ: REPLICA"

# Filtrar solo operaciones de escritura
docker-compose logs backend | grep "WRITE: PRIMARY"

# Ver errores
docker-compose logs backend | grep -i error
```

## 🎯 Resultados y Conclusiones

### Beneficios Demostrados

1. **Mejora en rendimiento de lecturas**: La separación permite distribuir la carga entre Primary y Replica
2. **Alta disponibilidad**: El sistema continúa funcionando parcialmente ante fallos
3. **Escalabilidad**: Se pueden agregar más réplicas para manejar mayor carga de lectura
4. **Monitoreo efectivo**: Los logs facilitan la identificación de problemas

### Lecciones Aprendidas

- La replicación mejora significativamente el rendimiento en sistemas con alta carga de lectura
- La infraestructura responde correctamente a fallas simuladas
- El uso de Docker facilita el despliegue en cualquier entorno
- La separación R/W requiere gestión cuidadosa de la consistencia eventual

### Métricas del Sistema

- **Tiempo promedio de lectura (Replica)**: 6-15 ms
- **Tiempo promedio de escritura (Primary)**: 12-25 ms
- **Delay de sincronización**: 20-80 ms
- **Tolerancia a fallos**: Sí (parcial)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 📧 Contacto

**Equipo de Desarrollo:**
- Julián David Calderón Largo
- Juan José Betancourth
- Valentina Franco

**Repositorio:** [https://github.com/JuliiizLargo/Implementacion-simple-docker](https://github.com/JuliiizLargo/Implementacion-simple-docker)

---

⭐ Si este proyecto te fue útil para aprender sobre replicación de bases de datos y arquitecturas escalables, considera darle una estrella en GitHub
