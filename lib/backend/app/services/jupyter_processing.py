import os
import nbformat
from nbconvert import LatexExporter
from nbconvert.preprocessors import ExtractOutputPreprocessor
from traitlets.config import Config
from html2image import Html2Image
from PIL import Image
import uuid
import logging
import base64
import time
import shutil
import random
import io
from app.utils.file_utils import ensure_directory_exists


# Configure logging
def setup_logging(output_dir, log_file="jupyter_processing.log"):
    ensure_directory_exists(output_dir)
    log_file_path = os.path.join(output_dir, log_file)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, mode='w', encoding='utf-8'), 
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def extract_images(notebook, output_dir, prefix):
    """Extract images from the notebook and ensure unique filenames."""
    ensure_directory_exists(output_dir)

    for i, cell in enumerate(notebook.cells):
        if 'outputs' not in cell:
            continue
        for o, output in enumerate(cell['outputs']):
            if 'metadata' not in output or 'image/png' not in output.get('data', {}):
                continue

            # Generate a truly unique filename
            unique_filename = f"{prefix}_cell{i}_output{o}_{prefix+i+o}.png"
            complete_filename = os.path.normpath(os.path.join(output_dir, unique_filename))

            try:
                content = output['data']['image/png']

                # Convert base64 string to bytes if needed
                if isinstance(content, str):
                    content = base64.b64decode(content)

                # Validate image content before saving
                try:
                    Image.open(io.BytesIO(content)).verify()
                except Exception as e:
                    logging.error(f"Invalid image content in cell {i}, output {o}: {e}")
                    continue

                with open(complete_filename, "wb") as image_file:
                    image_file.write(content)

                logging.info(f"Saved image: {complete_filename}")
                output['metadata']['filenames'] = {'image/png': unique_filename}
            except Exception as e:
                logging.error(f"Error saving image {unique_filename}: {e}")

def extract_html_displays(notebook, output_dir, prefix):
    """Extract and render HTML displays as images."""
    output_dir = os.path.normpath(output_dir)
    ensure_directory_exists(output_dir)

    # Check for Chrome installation
    chrome_path = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium")
    if chrome_path is None:
        logging.error("Chrome is either not installed or not available in the system PATH.")
        return

    try:
        # Initialize Html2Image with the path to the Chrome executable
        hti = Html2Image(browser_executable=chrome_path, output_path=output_dir, size=(1920, 1080))
    except Exception as e:
        logging.error(f"Failed to initialize Html2Image: {e}")
        return

    logging.info(f"Output directory set to: {output_dir}")

    for i, cell in enumerate(notebook.cells):
        if 'outputs' not in cell:
            continue
        for o, output in enumerate(cell['outputs']):
            html_content = output.get('data', {}).get('text/html', None)
            if html_content is None:
                continue

            # Create a unique filename
            unique_filename = f"{prefix}_cell{i}_output{o}_{int(time.time())}_{uuid.uuid4().hex}_{random.randint(1000,9999)}.png"
            image_path = os.path.normpath(os.path.join(output_dir, unique_filename))

            try:
                logging.info(f"Rendering HTML from cell {i}, output {o}: {html_content[:500]}")

                # Convert HTML to an image
                hti.screenshot(html_str=html_content, save_as=unique_filename)

                # Validate if the image file was saved
                if not os.path.exists(image_path):
                    logging.error(f"Failed to save image: {image_path}")
                    continue

                # Open and process the image
                with Image.open(image_path) as img:
                    img = img.convert('RGB')  # Convert image to RGB format
                    img.save(image_path, format='PNG')  # Save as PNG

                logging.info(f"HTML successfully rendered to image: {image_path}")
            except Exception as e:
                logging.error(f"Error rendering HTML in cell {i}, output {o}: {e}")

def modify_output_filenames(notebook, prefix):
    """
    Ensure unique filenames for all output images to prevent overwriting issues.
    """
    seen_filenames = set()

    for i, cell in enumerate(notebook.cells):
        if 'outputs' not in cell:
            continue

        for o, output in enumerate(cell['outputs']):
            if 'metadata' not in output:
                output['metadata'] = {}

            if 'filenames' not in output['metadata']:
                output['metadata']['filenames'] = {}

            # Generate a unique filename
            while True:
                unique_filename = f"{prefix}_cell{i}_output{o}_{int(time.time())}_{uuid.uuid4().hex}_{random.randint(1000,9999)}.png"
                if unique_filename not in seen_filenames:
                    seen_filenames.add(unique_filename)
                    break

            output['metadata']['filenames']['image/png'] = unique_filename

            logging.info(f"Updated filename metadata for cell {i}, output {o} to {unique_filename}")

def convert_jupyter_to_latex(notebook_file, output_dir):
    """Convert Jupyter Notebook to LaTeX while ensuring unique image filenames."""
    logger = setup_logging(output_dir)
    ensure_directory_exists(output_dir)

    try:
        # Read and process the notebook
        with open(notebook_file, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        logging.info(f"Processing notebook: {notebook_file}")

        base_name = os.path.splitext(os.path.basename(notebook_file))[0]
        modify_output_filenames(notebook, base_name)
        extract_images(notebook, output_dir, base_name)
        extract_html_displays(notebook, output_dir, base_name)

        c = Config()
        c.LatexExporter.preprocessors = [ExtractOutputPreprocessor]
        exporter = LatexExporter(config=c)

        (body, _) = exporter.from_notebook_node(notebook)
        output_path = os.path.normpath(os.path.join(output_dir, f"{base_name}.tex"))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(body)

        logging.info(f"LaTeX file written to {output_path}")
        return output_path

    except Exception as e:
        logging.error(f"Failed to convert notebook to LaTeX: {e}")
        raise