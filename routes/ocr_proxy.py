from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response, JSONResponse
import httpx
import traceback

router = APIRouter()

@router.post("/ocr/proxy/{endpoint}")
async def ocr_proxy(endpoint: str, file: UploadFile = File(...)):
    try:
        print(f"[INFO] Incoming request for endpoint: {endpoint}")
        file_bytes = await file.read()
        filename = file.filename
        content_type = file.content_type or 'application/pdf'
        print(f"[INFO] File received: {filename}, type: {content_type}")

        url = f"https://clickscanstg.terralogic.com/ocr/{endpoint}/"
        print(f"[INFO] Sending request to: {url}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                files={"file": (filename, file_bytes, content_type)},
                headers={"Accept": "application/json"}
            )

        print(f"[INFO] Upstream response status: {response.status_code}")
        print(f"[INFO] Response headers: {response.headers}")
        print(f"[INFO] Response content: {response.text}")

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("Content-Type", "application/json")
        )

    except Exception as e:
        print("[ERROR] Exception occurred:")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
