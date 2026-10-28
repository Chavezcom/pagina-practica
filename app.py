from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Mi Primera Web con FastAPI</title>
        </head>
        <body>
            <h1>¡Hola, mundo desde FastAPI!</h1>
            <p>Esta es mi primera página web.</p>
        </body>
    </html>
    """