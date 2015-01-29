# -*- coding: utf-8 -*-
import json
import unittest

import deezer
from mock import patch
from .mocked_methods import fake_urlopen


class TestResources(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('deezer.client.urlopen', fake_urlopen)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_resource_dict(self):
        """
        Test that resource can be converted to dict
        """
        client = deezer.Client()
        response = fake_urlopen(client.object_url('track', 3135556))
        resp_str = response.read().decode('utf-8')
        response.close()
        data = json.loads(resp_str)
        resource = deezer.resources.Resource(client, data)
        self.assertEqual(resource._asdict(), data)

    def test_resource_relation(self):
        """
        Test passing parent object when using get_relation
        """
        client = deezer.Client()
        album = client.get_album(302127)
        tracks = album.get_tracks()
        self.assertTrue(tracks[0].album is album)

    def test_album_attributes(self):
        """
        Test album resource
        """
        client = deezer.Client()
        album = client.get_album(302127)
        self.assertTrue(hasattr(album, 'title'))
        self.assertEqual(repr(album), '<Album: Discovery>')
        artist = album.get_artist()
        self.assertIsInstance(artist, deezer.resources.Artist)
        self.assertEqual(repr(artist), '<Artist: Daft Punk>')

    def test_album_tracks(self):
        """
        Test tracks method of album resource
        """
        client = deezer.Client()
        album = client.get_album(302127)
        tracks = album.get_tracks()
        self.assertIsInstance(tracks, list)
        track = tracks[0]
        self.assertIsInstance(track, deezer.resources.Track)
        self.assertEqual(repr(track), '<Track: One More Time>')

    def test_artist_attributes(self):
        """
        Test artist resource
        """
        client = deezer.Client()
        artist = client.get_artist(27)
        self.assertTrue(hasattr(artist, 'name'))
        self.assertIsInstance(artist, deezer.resources.Artist)
        self.assertEqual(repr(artist), '<Artist: Daft Punk>')

    def test_artist_albums(self):
        """
        Test albums method of artist resource
        """
        client = deezer.Client()
        artist = client.get_artist(27)
        albums = artist.get_albums()
        self.assertIsInstance(albums, list)
        album = albums[0]
        self.assertIsInstance(album, deezer.resources.Album)
        self.assertEqual(repr(album),
                         '<Album: Human After All (Remixes) (Remixes)>')

    def test_artist_top(self):
        """
        Test top method of artist resource
        """
        client = deezer.Client()
        artist = client.get_artist(27)
        tracks = artist.get_top()
        self.assertIsInstance(tracks, list)
        track = tracks[0]
        self.assertIsInstance(track, deezer.resources.Track)
        self.assertEqual(repr(track), '<Track: Get Lucky (Radio Edit)>')

    def test_artist_radio(self):
        """
        Test radio method of artist resource
        """
        client = deezer.Client()
        artist = client.get_artist(27)
        tracks = artist.get_radio()
        self.assertIsInstance(tracks, list)
        track = tracks[0]
        self.assertIsInstance(track, deezer.resources.Track)
        self.assertEqual(repr(track), '<Track: Lose Yourself to Dance>')

    def test_artist_related(self):
        """
        Test related method of artist resource
        """
        client = deezer.Client()
        artist = client.get_artist(27)
        artists = artist.get_related()
        self.assertIsInstance(artists, list)
        artist = artists[0]
        self.assertIsInstance(artist, deezer.resources.Artist)
        self.assertEqual(repr(artist), '<Artist: Justice>')

    def test_track_attributes(self):
        """
        Test track resource
        """
        client = deezer.Client()
        track = client.get_track(3135556)
        artist = track.get_artist()
        album = track.get_album()
        self.assertTrue(hasattr(track, 'title'))
        self.assertIsInstance(track, deezer.resources.Track)
        self.assertIsInstance(artist, deezer.resources.Artist)
        self.assertIsInstance(album, deezer.resources.Album)
        self.assertEqual(repr(track), '<Track: Harder Better Faster Stronger>')
        self.assertEqual(repr(artist), '<Artist: Daft Punk>')
        self.assertEqual(repr(album), '<Album: Discovery>')

    def test_radio_attributes(self):
        """
        Test radio resource
        """
        client = deezer.Client()
        radio = client.get_radio(23261)
        self.assertTrue(hasattr(radio, 'title'))
        self.assertIsInstance(radio, deezer.resources.Radio)
        self.assertEqual(repr(radio), '<Radio: Telegraph Classical>')

    def test_radio_tracks(self):
        """
        Test tracks method of radio resource
        """
        client = deezer.Client()
        radio = client.get_radio(23261)
        tracks = radio.get_tracks()
        self.assertIsInstance(tracks, list)
        track = tracks[2]
        self.assertIsInstance(track, deezer.resources.Track)
        self.assertEqual(repr(track), '<Track: Schumann: Kinderszenen, Op.15 - 11. Fürchtenmachen>')

    def test_genre_attributes(self):
        """
        Test genre resource
        """
        client = deezer.Client()
        genre = client.get_genre(106)
        self.assertTrue(hasattr(genre, 'name'))
        self.assertIsInstance(genre, deezer.resources.Genre)
        self.assertEqual(repr(genre), '<Genre: Electro>')

    def test_genre_artists(self):
        """
        Test artists method of genre resource
        """
        client = deezer.Client()
        genre = client.get_genre(106)
        artists = genre.get_artists()
        self.assertIsInstance(artists, list)
        artist = artists[0]
        self.assertIsInstance(artist, deezer.resources.Artist)
        self.assertEqual(repr(artist), '<Artist: Calvin Harris>')

    def test_genre_radios(self):
        """
        Test radios method of genre resource
        """
        client = deezer.Client()
        genre = client.get_genre(106)
        radios = genre.get_radios()
        self.assertIsInstance(radios, list)
        radio = radios[0]
        self.assertIsInstance(radio, deezer.resources.Radio)
        self.assertEqual(repr(radio), '<Radio: Techno/House>')
