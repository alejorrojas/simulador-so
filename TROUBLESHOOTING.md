# Solución de Problemas - Simulador de Memoria

Este documento contiene soluciones a problemas comunes al ejecutar los ejecutables del simulador.

## Índice

- [Problema en Windows: Error de módulo rich](#problema-en-windows-error-de-módulo-rich)
- [Problema en macOS: Ejecutable bloqueado por seguridad](#problema-en-macos-ejecutable-bloqueado-por-seguridad)
- [Problemas con archivos CSV](#problemas-con-archivos-csv)

---

## Problema en Windows: Error de módulo rich

### Síntoma

Al ejecutar el programa aparece un error:

```
Error inesperado: No module named 'rich._unicode_data.unicode17-0-0'
```

### Causa

PyInstaller no incluyó correctamente los archivos de datos Unicode de la biblioteca `rich` que se necesitan para Python 3.13.

### Solución

Este problema ha sido corregido en el workflow de compilación. Para obtener el ejecutable corregido:

1. **Si tienes acceso al repositorio**: Descarga la última versión de los ejecutables desde GitHub Actions después del próximo build.

2. **Si solo tienes el ZIP**: Contacta al equipo de desarrollo para obtener la versión actualizada.

3. **Alternativa temporal**: Ejecuta el programa desde el código fuente:
   ```bash
   # En Windows (PowerShell o CMD)
   pip install rich
   python src/main.py
   ```

---

## Problema en macOS: Ejecutable bloqueado por seguridad

### Síntoma

Al intentar ejecutar el programa aparece una alerta de seguridad:

```
"simulador-memoria-macos-arm" No se puede abrir
Apple no puede verificar que "simulador-memoria-macos-arm" esté libre de malware
```

### Causa

macOS Gatekeeper bloquea ejecutables que no están firmados digitalmente con un certificado de desarrollador de Apple.

### Solución

Tienes **3 opciones**:

#### Opción 1: Permitir la ejecución desde Configuración del Sistema (Recomendado)

1. **Intenta abrir el ejecutable** normalmente (doble clic o desde Terminal)
2. **Aparecerá el mensaje de seguridad** - haz clic en "Cancelar" o "Cerrar"
3. **Abre Configuración del Sistema**:
   - Ve a  (menú Apple) → **Configuración del Sistema**
   - Ve a **Privacidad y Seguridad**
4. **Desplázate hacia abajo** hasta la sección "Seguridad"
5. **Busca el mensaje** sobre "simulador-memoria-macos-arm"
6. **Haz clic en "Abrir de todas formas"** o **"Allow Anyway"**
7. **Confirma** tu decisión en el siguiente diálogo
8. **Intenta ejecutar el programa nuevamente**

#### Opción 2: Eliminar el atributo de cuarentena (Más rápido)

Abre la Terminal y ejecuta:

```bash
# Navega a la carpeta donde está el ejecutable
cd /ruta/donde/descargaste/el/ejecutable

# Elimina el atributo de cuarentena
xattr -d com.apple.quarantine simulador-memoria-macos-arm

# Dale permisos de ejecución
chmod +x simulador-memoria-macos-arm

# Ejecuta el programa
./simulador-memoria-macos-arm
```

#### Opción 3: Ejecutar desde el código fuente (Si tienes Python instalado)

```bash
# Instala las dependencias
pip install rich

# Ejecuta el programa
python src/main.py
```

### Por qué es seguro

El ejecutable es seguro porque:
- ✅ El código fuente está disponible en el repositorio para inspección
- ✅ Fue compilado automáticamente por GitHub Actions (proceso transparente)
- ✅ No contiene malware ni código malicioso
- ⚠️ Simplemente **no tiene firma digital** porque requiere una cuenta de desarrollador de Apple ($99/año)

---

## Problemas con archivos CSV

### El programa no reconoce el archivo CSV

**Solución**: Verifica que el archivo tenga exactamente estas columnas:

```csv
proceso_id,t_arribo_al_sistema,memoria_K,tiempo_irrupcion
P1,0,200,5
P2,1,50,3
```

### Error: "No se encontró el archivo"

**Solución**:

1. **Verifica la ruta**: Usa rutas absolutas o coloca el CSV en la misma carpeta que el ejecutable
2. **Puedes usar comillas**: Las rutas con espacios ahora funcionan con o sin comillas:
   - ✅ `C:\Users\Mi Usuario\procesos.csv`
   - ✅ `"C:\Users\Mi Usuario\procesos.csv"`
3. **En macOS/Linux**: Puedes usar `~` para el directorio home:
   - ✅ `~/Desktop/procesos.csv`

### Error: "Debe ingresar una ruta de archivo"

**Solución**: El programa esperaba que hubiera un archivo `procesos.csv` en la carpeta actual. Debes:
- Ingresar la ruta completa del archivo, o
- Crear un archivo `procesos.csv` en la misma carpeta que el ejecutable

---

## ¿Necesitas más ayuda?

Si ninguna de estas soluciones funciona, por favor:

1. Anota el mensaje de error completo
2. Indica tu sistema operativo y versión
3. Describe los pasos que seguiste
4. Contacta al equipo de desarrollo

---

**Última actualización**: Febrero 2025
