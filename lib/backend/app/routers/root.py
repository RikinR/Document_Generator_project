from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Welcome to the File Processing API!

    This API allows you to upload LaTeX, PowerPoint, and Jupyter Notebook files, which are then processed, merged, and compiled into a single PDF document.

    ### Usage
    - Use the **POST /process/** endpoint to upload files and generate a PDF.
    - Supported file types: `.tex`, `.pptx`, `.ipynb`.
    """
    return HTMLResponse("""
    <html>
        <head><title>File Processing API</title></head>
        <body>
            <h1>File Processing Service</h1>
            <p>Upload LaTeX, PowerPoint, or Jupyter Notebook files to generate a merged PDF.</p>
            <h2>API Documentation</h2>
            <ul>
                <li><strong>GET /</strong>: Returns this welcome page.</li>
                <li><strong>POST /process/</strong>: Accepts LaTeX, PowerPoint, and Jupyter Notebook files and returns a merged PDF.</li>
            </ul>
        </body>
    </html>
    """)