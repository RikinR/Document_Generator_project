import unittest
import os

from backend.app.services.latex_processing import compile_latex_to_pdf, escape_latex_special_chars, merge_latex_files


class TestLatexProcessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = "tmp"
        os.makedirs(self.temp_dir, exist_ok=True)

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_escape_latex_special_chars(self):
        text = "This is a test & % $ # _ { } ~ ^ \\ < > |"
        escaped_text = escape_latex_special_chars(text)
        expected_text = r"This is a test \& \% \$ \# \_ \{ \} \textasciitilde{} \^{} \textbackslash{} \textless{} \textgreater{} \textbar{}"
        self.assertEqual(escaped_text, expected_text)

    def test_merge_latex_files(self):
        latex_file1 = os.path.join(self.temp_dir, "file1.tex")
        latex_file2 = os.path.join(self.temp_dir, "file2.tex")

        with open(latex_file1, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\nHello, World!\n\\end{document}")

        with open(latex_file2, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\nGoodbye, World!\n\\end{document}")

        
        output_file = os.path.join(self.temp_dir, "merged.tex")
        merge_latex_files([latex_file1, latex_file2], output_file)

        self.assertTrue(os.path.exists(output_file))

    def test_compile_latex_to_pdf(self):
        latex_file = os.path.join(self.temp_dir, "test.tex")
        with open(latex_file, "w") as f:
            f.write("\\documentclass{article}\n\\begin{document}\nHello, World!\n\\end{document}")

        success, message = compile_latex_to_pdf(latex_file, self.temp_dir)

        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "test.pdf")))

if __name__ == "__main__":
    unittest.main()