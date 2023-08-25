export const environment = {
  production: true,
  serverUrl: 'http://localhost:9000',
  endPoints: {
    videoSearchEndPoints: {
      searchVideosEndPoint: '/search?query={query}'
    },
    audioPlayerEndPoints: {
      playAudioSampleEndPoint: '/player/videos/{videoId}',
      playUserSavedAudioEndPoint: '/player/users/{userId}/recordings/{recordingId}'
    },
    userAudioEndPoints: {
      saveUserAudioRecordingEndPoint: '/audio/users/{userId}/videos/{videoId}',
      getAllUserAudioRecordingsEndPoint: '/audio/users/{userId}/recordings',
      deleteUserAudioRecordingEndPoint: '/audio/users/{userId}/recordings/{recordingId}',
      downloadUserAudioRecordingEndPoint: '/audio/users/{userId}/recordings/{recordingId}'
    }
  }
};
