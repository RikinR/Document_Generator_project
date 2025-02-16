import os
import re
import subprocess

def escape_latex_special_chars(text: str) -> str:
    """
    Escape special LaTeX characters and remove control characters.
    """
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', text)
    
    # Escape LaTeX special characters
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
        '|': r'\textbar{}',
    }
    return re.sub(
        r'[&%$#_{}~^\\<>|]',
        lambda m: special_chars[m.group()],
        text
    )

def merge_latex_files(latex_files: list, output_file: str):
    """
    Merge multiple LaTeX files into one document with proper structure.
    """
    essential_preamble = [
        r"\documentclass{article}",
        r"\usepackage{enumitem}",
        r"\setlistdepth{8}",  
        r"\setlist[itemize,1]{label=\textbullet}",
        r"\setlist[itemize,2]{label=--}",
        r"\setlist[itemize,3]{label=*}",
        r"\setlist[itemize,4]{label=-}",
        r"\setlist[itemize,5]{label=$\cdot$}",  
        r"\setlist[itemize,6]{label=$\diamond$}",  
        r"\setlist[itemize,7]{label=$\ast$}",  
        r"\setlist[itemize,8]{label=$\circ$}", 
        r"\usepackage{ulem}",
        r"\usepackage{graphicx}",
        r"\usepackage{hyperref}",
        r"\usepackage{geometry}",
        r"\geometry{a4paper, margin=1in}",
    ]
    
    custom_preamble = []
    content = []

    for latex_file in latex_files:
        with open(latex_file, "r", encoding="utf-8") as infile:
            in_preamble = True  # Start in the preamble
            for line in infile:
                line = line.strip()
                if line.startswith(r"\documentclass"):
                    continue  # Skip duplicate document classes
                if line.startswith(r"\usepackage"):
                    # Extract the package name using regex
                    match = re.search(r'\\usepackage\{(.*?)\}', line)
                    if match:
                        package_name = match.group(1)
                        if not is_package_available(package_name):
                            print(f"Package {package_name} is not available. Ignoring.")
                            continue
                        if line not in essential_preamble and line not in custom_preamble:
                            custom_preamble.append(line)
                    else:
                        print(f"Warning: Could not parse package name from line: {line}")
                    continue
                if line.startswith(r"\begin{document}"):
                    in_preamble = False
                    continue
                if line.startswith(r"\end{document}"):
                    continue
                if in_preamble:
                    # Collect other preamble commands (e.g., \newcommand)
                    if line and not line.startswith("%"):  # Skip comments
                        custom_preamble.append(line)
                else:
                    # Collect content after \begin{document}
                    content.append(line + "\n")
            
            
            content.append("\n")

    # Build final preamble
    full_preamble = essential_preamble + custom_preamble + [r"\begin{document}"]

    # Write merged file
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(full_preamble) + "\n")
        outfile.write("".join(content))
        outfile.write(r"\end{document}" + "\n")

def is_package_available(package_name: str) -> bool:
    """
    Check if a LaTeX package is available in the system.
    """
    try:
        result = subprocess.run(
            ["kpsewhich", f"{package_name}.sty"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking package {package_name}: {e}")
        return False

def compile_latex_to_pdf(tex_file: str, output_dir: str) -> tuple[bool, str]:
    """
    Compile LaTeX document to PDF using XeLaTeX.
    Returns a tuple (success, message).
    """
    try:
        tex_file = tex_file.replace("\\", "/")
        output_dir = output_dir.replace("\\", "/")
        tex_file_name = os.path.basename(tex_file)

        log_file = os.path.join(output_dir, "latex_output.log")
        
        # Run XeLaTeX twice to resolve cross-references
        for _ in range(2):
            result = subprocess.run(
                ["xelatex", "-synctex=1", "-interaction=nonstopmode", tex_file_name],
                cwd=output_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            
            # Write output to log file
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(result.stdout)
                if result.returncode != 0:
                    f.write(f"\nXeLaTeX exited with code {result.returncode}")

        if result.returncode != 0:
            # Check if the error is due to missing packages
            if "LaTeX Error: File `" in result.stdout:
                print("Warning: Some packages are missing, but proceeding with compilation.")
            else:
                return False, f"XeLaTeX failed with exit code {result.returncode}"

        pdf_file = os.path.splitext(tex_file)[0] + ".pdf"
        if not os.path.exists(pdf_file):
            return False, f"PDF file not generated. Check log: {log_file}"

        return True, "Compilation successful."
            
    except Exception as e:
        error_msg = f"LaTeX compilation error: {str(e)}"
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                error_msg += f"\n\nLog Output:\n{f.read()}"
        return False, error_msg