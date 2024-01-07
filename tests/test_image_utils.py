import os
import shutil
import unittest
from unittest import mock
from datetime import datetime
from src.utils.image_utils import (
    get_new_filename, ensure_folder_exists, convert_single_image_to_webp
)

class TestImageUtils(unittest.TestCase):

    def test_get_new_filename(self):
        """
        Test get_new_filename function to ensure it generates correct filenames.
        """
        test_path = "test/sample.jpg"
        quality = 80
        result = get_new_filename(test_path, quality)
        timestamp = datetime.now().strftime("%Y%m%d")
        self.assertIn(timestamp, result)
        self.assertIn(str(quality), result)
        self.assertTrue(result.endswith(".webp"))

    def test_ensure_folder_exists(self):
        """
        Test ensure_folder_exists to verify it creates a folder if it does not exist.
        """
        test_folder = "test_folder"
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)  # Ensure the folder is deleted if it exists

        self.assertFalse(os.path.exists(test_folder))
        ensure_folder_exists(test_folder)
        self.assertTrue(os.path.exists(test_folder))
        shutil.rmtree(test_folder)  # Cleanup after test

    @mock.patch('src.utils.image_utils.Image')
    def test_convert_single_image_to_webp(self, mock_image):
        """
        Test convert_single_image_to_webp to verify it handles non-GIF images correctly.
        """
        test_path = "test/sample.jpg"
        output_path = "output"
        quality = 80
        test_queue = mock.Mock()

        # Setup: Create a temporary output directory
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        convert_single_image_to_webp(test_path, output_path, quality, test_queue)
        test_queue.put.assert_called_with(f"Converted image: {os.path.join(output_path, get_new_filename(test_path, quality))}")

        # Cleanup
        shutil.rmtree(output_path)


if __name__ == '__main__':
    unittest.main()
