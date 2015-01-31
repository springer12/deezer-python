import deezer
import unittest
import tornado.gen
import tornado.ioloop
from mock import patch
from .mocked_methods import fake_urlopen


class TestClient(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('deezer.client.urlopen', fake_urlopen)
        self.patcher.start()
        self.client = deezer.Client(app_id='foo', app_secret='bar')
        self.unsec_client = deezer.Client(use_ssl=False)

    def tearDown(self):
        self.patcher.stop()

    def test_kwargs_parsing_valid(self):
        """Test that valid kwargs are stored as properties on the client."""
        self.assertEqual(self.client.app_id, 'foo')
        self.assertEqual(self.client.app_secret, 'bar')

    def test_ssl(self):
        """Test that the ssl parameter provides the right scheme"""
        self.assertEqual(self.client.scheme, 'https')
        self.assertEqual(self.unsec_client.scheme, 'http')

    def test_url(self):
        """Test the url() method
        it should add / to the request if not present
        """
        self.client.url()
        user = self.client.url('/user')
        self.assertEqual(user, "https://api.deezer.com/user")
        user = self.client.url('user')
        self.assertEqual(user, "https://api.deezer.com/user")

    def test_object_url(self):
        """Test the object_url() method, validates against the allowed types
        of objects"""
        self.assertEqual(self.client.object_url("album"),
                         "https://api.deezer.com/album")
        self.assertEqual(self.client.object_url("album", 12),
                         "https://api.deezer.com/album/12")
        self.assertEqual(self.client.object_url("album", "12"),
                         "https://api.deezer.com/album/12")
        self.assertEqual(self.client.object_url("album", "12", "artist"),
                         "https://api.deezer.com/album/12/artist")
        self.assertEqual(self.client.object_url("album", "12", limit=1),
                         "https://api.deezer.com/album/12?limit=1")
        self.assertEqual(self.client.object_url("album", "12", "artist",
                         limit=1),
                         "https://api.deezer.com/album/12/artist?limit=1")
        self.assertRaises(TypeError, self.client.object_url, 'foo')

    def test_get_album(self):
        """Test method to retrieve an album"""
        album = self.client.get_album(302127)
        self.assertIsInstance(album, deezer.resources.Album)

    def test_get_artist(self):
        """Test methods to get an artist"""
        artist = self.client.get_artist(27)
        self.assertIsInstance(artist, deezer.resources.Artist)

    def test_get_comment(self):
        """Test methods to get a comment"""
        comment = self.client.get_comment(2772704)
        self.assertIsInstance(comment, deezer.resources.Comment)

    def test_get_genre(self):
        """Test methods to get a genre"""
        genre = self.client.get_genre(106)
        self.assertIsInstance(genre, deezer.resources.Genre)

    def test_get_genres(self):
        """Test methods to get several genres"""
        genres = self.client.get_genres()
        self.assertIsInstance(genres, list)
        self.assertIsInstance(genres[0], deezer.resources.Genre)

    def test_get_playlist(self):
        """Test methods to get a playlist"""
        playlist = self.client.get_playlist(223)
        self.assertIsInstance(playlist, deezer.resources.Playlist)

    def test_get_radio(self):
        """Test methods to get a radio"""
        radio = self.client.get_radio(23261)
        self.assertIsInstance(radio, deezer.resources.Radio)

    def test_get_radios(self):
        """Test methods to get a radios"""
        radios = self.client.get_radios()
        self.assertIsInstance(radios, list)
        self.assertIsInstance(radios[0], deezer.resources.Radio)

    def test_get_track(self):
        """Test methods to get a track"""
        track = self.client.get_track(3135556)
        self.assertIsInstance(track, deezer.resources.Track)

    def test_get_user(self):
        """Test methods to get a user"""
        user = self.client.get_user(359622)
        self.assertIsInstance(user, deezer.resources.User)

    def test_search(self):
        """Test search method"""
        self.assertEqual(self.client.object_url("search", q="Daft Punk"),
                         "https://api.deezer.com/search?q=Daft+Punk")
        result = self.client.search("Billy Jean")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Billy Jean")

        self.assertEqual(self.client.object_url("search",
                         relation="track", q="Daft Punk"),
                         "https://api.deezer.com/search/track?q=Daft+Punk")
        result = self.client.search("Billy Jean", "track")
        self.assertIsInstance(result, list)
        self.assertEqual(result[0].title, "Billy Jean")
        self.assertIsInstance(result[0], deezer.resources.Track)

    def test_options(self):
        """Test a query with extra arguments"""
        result = self.client.search("Billy Jean", limit=2)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 2)

        result = self.client.search("Billy Jean", limit=2, index=1)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 2)


class TestAsyncClient(unittest.TestCase):
    def setUp(self):
        self.client = deezer.AsyncClient()

    def test_get_object(self):
        @tornado.gen.coroutine
        def callback():
            album = yield self.client.get_album(302127)
            self.assertIsInstance(album, deezer.resources.Album)
            tracks = yield album.get_tracks()
            self.assertTrue(tracks[0].album is album)

        tornado.ioloop.IOLoop.instance().run_sync(callback)


if __name__ == '__main__':
    unittest.main()
