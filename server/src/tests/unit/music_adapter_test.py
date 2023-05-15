from youtube_music_manager_server.adapters.music_adapter import MusicAdapter
from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.dtos.song_dto import SongDto
from youtube_music_manager_server.persistence.domain.database_song import DatabaseSong


class MusicAdapterTest:

    @staticmethod
    def test_input_is_adapted(unit_tests_song: Song, music_adapter: MusicAdapter) -> None:

        song_id = unit_tests_song.id
        input_data = {'title': unit_tests_song.title, 'artist': unit_tests_song.artist}
        result = music_adapter.adapt_input(song_id, input_data)

        assert isinstance(result, SongDto)
        assert result.id == song_id
        assert result.title == input_data['title']
        assert result.artist == input_data['artist']

    @staticmethod
    def test_persistence_is_adapted(unit_tests_song: Song, music_adapter: MusicAdapter) -> None:

        database_song = music_adapter.adapt_to_persist(unit_tests_song)

        assert isinstance(database_song, DatabaseSong)
        assert database_song.id == unit_tests_song.id
        assert database_song.title == unit_tests_song.title
        assert database_song.artist == unit_tests_song.artist
        assert database_song.file == unit_tests_song.file
        assert type(database_song.creation_date) == str

    @staticmethod
    def test_output_is_adapted(unit_tests_database_song: DatabaseSong, music_adapter: MusicAdapter) -> None:

        songs = [unit_tests_database_song]
        result = music_adapter.adapt_output(songs)

        assert type(result) == list
        assert len(result) == 1

        adapted_song = result[0]

        assert type(adapted_song) == dict
        assert adapted_song.get('id') == unit_tests_database_song.id
        assert adapted_song.get('title') == unit_tests_database_song.title
        assert adapted_song.get('artist') == unit_tests_database_song.artist
