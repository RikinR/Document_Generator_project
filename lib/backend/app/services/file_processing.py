import shutil
import os
from typing import List
from fastapi import UploadFile
from app.services.latex_processing import merge_latex_files, compile_latex_to_pdf
from app.services.ppt_processing import convert_pptx_to_latex
from app.services.jupyter_processing import convert_jupyter_to_latex

TEMP_DIR = "tmp"

async def process_files(latex: List[UploadFile], ppt: List[UploadFile], notebook: List[UploadFile]):
    """z
    Process uploaded files and generate a merged PDF.
    """
    # Clear and recreate the temp directory
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    file_paths = {
        "latex": [],
        "ppt": [],
        "notebook": []
    }

    # Save uploaded files
    for file_type, files in [("latex", latex), ("ppt", ppt), ("notebook", notebook)]:
        if files:
            for i, file in enumerate(files):
                ext = {
                    "latex": ".tex",
                    "ppt": ".pptx",
                    "notebook": ".ipynb"
                }[file_type]
                
                file_path = os.path.join(TEMP_DIR, f"{file_type}_{i}{ext}")
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                file_paths[file_type].append(file_path)

    # Process PowerPoint files
    for ppt_path in file_paths["ppt"]:
        convert_pptx_to_latex(ppt_path, TEMP_DIR)

    # Process Jupyter Notebook files
    for notebook_path in file_paths["notebook"]:
        convert_jupyter_to_latex(notebook_path, TEMP_DIR)

    # Collect all LaTeX files
    latex_files = []
    latex_files.extend(file_paths["latex"])
    latex_files.extend([os.path.join(TEMP_DIR, f"ppt_{i}.tex") for i in range(len(file_paths["ppt"]))])
    latex_files.extend([os.path.join(TEMP_DIR, f"notebook_{i}.tex") for i in range(len(file_paths["notebook"]))])

    # Merge and compile LaTeX files
    merged_tex_path = os.path.join(TEMP_DIR, "merged.tex")
    merge_latex_files(latex_files, merged_tex_path)
    compile_latex_to_pdf(merged_tex_path, TEMP_DIR)

    # Return the path to the generated PDF
    return os.path.join(TEMP_DIR, "merged.pdf")