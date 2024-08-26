import unittest
from app import app, db, Movie, User


class TestWatchList(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        db.create_all()
        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2020')
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        # self.assertEqual(response.status_code, 404)
        self.assertIn('Page Not Found - ', data)
        self.assertIn('Go Back', data)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Movie Title', data)
        self.assertIn('Test\'s Watchlist', data)

    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)

    def test_create_item(self):
        self.login()

        response = self.client.post('/', data=dict(
            title='New movie',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item created',data)
        self.assertIn('New movie',data)

        response = self.client.post('/', data=dict(
            title='',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)
        self.assertIn('Invalid title or year', data)

        response = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created', data)
        self.assertIn('Invalid title or year', data)

    def test_update_item(self):
        self.login()

        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2020', data)

        response = self.client.post('/movie/edit/1', data=dict(
            title='New Updated',
            year='2022'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item updated', data)
        self.assertIn('New Updated', data)

        response = self.client.post('/movie/edit/1', data=dict(
            title='',
            year='2022'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated', data)
        self.assertIn('Invalid input.', data)

        response = self.client.post('/movie/edit/1', data=dict(
            title='New Updated',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated', data)
        self.assertIn('Invalid input.', data)

    def  test_delete_movie(self):
        self.login()

        response = self.client.post('/movie/delete/1',follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)

if __name__ == '__main__':
    unittest.main()