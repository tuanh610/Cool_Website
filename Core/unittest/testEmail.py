import unittest
from Core.mail.mailingModule import mailModule

class TestEmail(unittest.TestCase):

    def setUp(self) -> None:
        self.mail = mailModule()

    def test_sendTextMail(self):
        try:
            service = self.mail.getCredential()
            content = self.mail.create_message('warmboy610@gmai.com','tuanh.dang610@gmail.com', "Test mail text", "Hello unit test")
            result = self.mail.send_message(service, content)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail("Function raise exception: %s" % str(e))


    def test_sendMailWithAttachment(self):
        try:
            service = self.mail.getCredential()
            content = self.mail.create_message_with_attachment('warmboy610@gmai.com','tuanh.dang610@gmail.com', "Test mail text", "Hello unit test", "../testdata/test.jpg")
            result = self.mail.send_message(service, content)
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail("Function raise exception: %s" % str(e))

if __name__ == '__main__':
    unittest.main()
