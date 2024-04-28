import unittest
from unittest.mock import patch, mock_open
from your_module import AuthenticationManager, FileStorageHandler, Student, Factory

class TestAuthenticationManager(unittest.TestCase):
    def test_singleton(self):
        manager1 = AuthenticationManager()
        manager2 = AuthenticationManager()
        self.assertEqual(manager1, manager2)

    def test_authenticate(self):
        manager = AuthenticationManager()
        self.assertTrue(manager.authenticate("admin", "password"))
        self.assertFalse(manager.authenticate("admin", "wrong_password"))

class TestFileStorageHandler(unittest.TestCase):
    def setUp(self):
        self.handler = Factory.get_storage_handler()

    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_file):
        data = {"key": "value"}
        self.handler.save(data)
        mock_file.assert_called_once_with('students.json', 'w')
        mock_file().write.assert_called_once()

    @patch('json.load')
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load(self, mock_file, mock_json_load):
        mock_json_load.return_value = {"key": "value"}
        self.assertEqual(self.handler.load(), {"key": "value"})

class TestStudent(unittest.TestCase):
    def test_student_initialization(self):
        student = Student("001", "John Doe", "1234567890", "123 Elm St", "A", "10")
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(student.phone_number, "1234567890")

    @patch("builtins.input", side_effect=["002", "Jane Doe", "0987654321", "321 Oak St", "B", "11"])
    def test_dynamic_student_initialization(self, mocked_input):
        student = Student()
        self.assertEqual(student.roll_no, "002")
        self.assertEqual(student.name, "Jane Doe")

    def test_update_student(self):
        student = Student("001", "John Doe", "1234567890", "123 Elm St", "A", "10")
        with patch("builtins.input", side_effect=["2", "9876543210"]):
            student.update_student()
            self.assertEqual(student.phone_number, "9876543210")

# Main function to run tests
if __name__ == '__main__':
    unittest.main()
