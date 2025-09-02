import unittest
from app.auth import login

class TestAuth(unittest.TestCase):
    
    def test_login_success(self):
        with self.client:
            response = self.client.post('/login', json={
                'username': 'admin',
                'password': 'adminpass'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome admin', response.get_data(as_text=True))

    def test_login_failure(self):
        with self.client:
            response = self.client.post('/login', json={
                'username': 'admin',
                'password': 'wrongpass'
            })
            self.assertEqual(response.status_code, 401)
            self.assertIn('Invalid credentials', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
