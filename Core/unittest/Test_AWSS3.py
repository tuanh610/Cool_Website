import unittest
import Core.storage.aws_s3 as aws_s3

class MyTestCase(unittest.TestCase):
    def test_uploadFile(self):
        file_name = "..\\testdata\\test.jpg"
        bucket = "imagestore.tuanh1234"
        self.assertTtrue(aws_s3.upload_file(file_name, bucket))

if __name__ == '__main__':
    unittest.main()
