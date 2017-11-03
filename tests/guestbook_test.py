import os
import unittest
import tempfile
import guestbook as gb


class GuestTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, gb.app.config['DATABASE'] = tempfile.mkstemp()
        gb.app.testing = True
        self.app = gb.app.test_client()
        with gb.app.app_context():
            gb.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(gb.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
