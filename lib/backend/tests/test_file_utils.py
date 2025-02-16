import unittest
import os
import tempfile
import shutil
from backend.app.utils.file_utils import ensure_directory_exists

class TestFileUtils(unittest.TestCase):
    def setUp(self):
       
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        
        shutil.rmtree(self.test_dir)

    def test_ensure_directory_exists(self):
        
        new_dir = os.path.join(self.test_dir, "new_dir")
        ensure_directory_exists(new_dir)
        self.assertTrue(os.path.exists(new_dir))
        self.assertTrue(os.access(new_dir, os.W_OK))

    def test_ensure_directory_exists_existing(self):
       
        ensure_directory_exists(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertTrue(os.access(self.test_dir, os.W_OK))


if __name__ == "__main__":
    unittest.main()