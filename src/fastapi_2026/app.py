from pathlib import Path
from typing import Annotated, Generator, TypeAlias # <-- AÑADIDO TypeAlias
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from sqlmodel import SQLModel, Field, Session, create_engine, select
from pwdlib import PasswordHash

# ==========================================
# 1. CONFIGURACIÓN INICIAL Y BASE DE DATOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
sqlite_file_name = BASE_DIR / "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# CORREGIDO: Le decimos a Pylance que esto es un "Alias de Tipo"
SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# ==========================================
# 2. INICIALIZACIÓN DE LA APP
# ==========================================
app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key="mi_clave_super_secreta")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ==========================================
# 3. MODELOS Y SEGURIDAD
# ==========================================
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

password_hash = PasswordHash.recommended()

# ==========================================
# 4. RUTAS DE LA APLICACIÓN
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"titulo": "Mi web con DB", "user": request.session.get("user")},
    )

# --- REGISTRO ---
@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request) -> Response:
    if request.session.get("user"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request=request, name="register.html")

@app.post("/register")
async def register_post(
    request: Request, 
    session: SessionDep, 
    username: str = Form(...), 
    password: str = Form(...)
) -> Response:
    user_exists = session.exec(select(User).where(User.username == username)).first()
    if user_exists:
        return templates.TemplateResponse(
            request=request, 
            name="register.html", 
            context={"error": "El usuario ya existe"}
        )
    
    hashed_pw = password_hash.hash(password)
    
    new_user = User(username=username, hashed_password=hashed_pw)
    session.add(new_user)
    session.commit()
    
    request.session["user"] = new_user.username
    return RedirectResponse(url="/perfil", status_code=303)

# --- LOGIN ---
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request) -> Response:
    if request.session.get("user"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
async def login_post(
    request: Request, 
    session: SessionDep, 
    username: str = Form(...), 
    password: str = Form(...)
) -> Response:
    user = session.exec(select(User).where(User.username == username)).first()
    
    if not user or not password_hash.verify(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"error": "Usuario o contraseña incorrectos"}
        )
    
    request.session["user"] = user.username
    return RedirectResponse(url="/perfil", status_code=303)

# --- LOGOUT ---
@app.get("/logout")
async def logout(request: Request) -> Response:
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# --- PERFIL PROTEGIDO ---
@app.get("/perfil", response_class=HTMLResponse)
async def perfil(request: Request) -> Response:
    usuario = request.session.get("user")
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(
        request=request, 
        name="perfil.html", 
        context={"user": usuario}
    )