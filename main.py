from fastapi import FastAPI
from routes import ocr_proxy  # Make sure 'routes' is a folder with __init__.py, and ocr_proxy.py inside it

app = FastAPI(
    title="ClickScan OCR Middleware",
    description="FastAPI proxy service for forwarding OCR files to the ClickScan server.",
    version="1.0.0"
)

# Include the OCR Proxy router
app.include_router(ocr_proxy.router)
