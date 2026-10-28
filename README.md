
## ⚡ Ejecutar el proyecto desde cero

### 1. Clona o descarga el proyecto

```bash
git clone <url-del-repo>
cd fastapi_2026
```

Si te lo han pasado en un ZIP, descomprímelo y entra en la carpeta:
```bash
cd fastapi_2026
```

### 2. Sincroniza el entorno (el comando clave)

```bash
uv sync
```

**¿Qué hace?**
- Lee `uv.lock` y crea la carpeta `.venv` si no existe.
- Instala las dependencias **exactas** que había el autor original.
- Instala la versión de Python indicada en `.python-version`.

👉 **No hace falta activar el entorno.** `uv` lo gestiona solo.

### 3. Arranca el servidor de desarrollo

```bash
uv run fastapi dev app.py
```

Abre tu navegador en:

- 🌐 Página principal: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📚 Documentación interactiva (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

El servidor **recarga automáticamente** cada vez que guardes cambios en el código. Para detenerlo, pulsa `Ctrl+C`.

---

## 🧰 Comandos que usarás en el día a día

| Acción | Comando |
|---|---|
| Instalar todas las dependencias | `uv sync` |
| Añadir una dependencia nueva | `uv add nombre-paquete` |
| Quitar una dependencia | `uv remove nombre-paquete` |
| Ejecutar un script | `uv run python mi_script.py` |
| Ejecutar una herramienta (ej. pytest) | `uv run pytest` |
| Actualizar dependencias | `uv lock --upgrade` |
| Ver dependencias instaladas | `uv tree` |

> ⚠️ **Importante:** No uses `pip install` ni `python -m venv` manualmente. `uv` gestiona todo. Si tienes problemas con un paquete muy concreto, usa `uv add` primero; si falla la resolución, entonces sí puedes probar `uv pip install <paquete>` **solo como último recurso** (pero ojo: eso **no** queda registrado en `pyproject.toml`).



## 📚 Recursos útiles

- 📖 Documentación de uv: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- 📖 Documentación de FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- 📖 Jinja2: [https://jinja.palletsprojects.com/](https://jinja.palletsprojects.com/)

---

## ✅ TL;DR — Los 3 pasos imprescindibles

```bash
uv sync                                                # 1. Instalar todo
uv run fastapi dev src/fastapi_2026/main.py          # 2. Arrancar
# 3. Abrir http://127.0.0.1:8000 en el navegador
```
