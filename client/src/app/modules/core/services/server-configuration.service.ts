import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ServerConfigurationService {

  private _serverUrl: string = 'http://localhost:9000';

  public getSearchVideosUrl(searchQuery: string): string {
    return this._serverUrl + `/search?query=${encodeURIComponent(searchQuery)}`
  }

	public getPlayAudioSampleUrl(videoId: string): string {
    return this._serverUrl + `/player/videos/${videoId}`
  }

	public getPlayUserSavedAudioUrl(userId: string, recordingId: string): string {
    return this._serverUrl + `/player/users/${userId}/recordings/${recordingId}`
  }

	public getSaveUserAudioRecordingUrl(userId: string, videoId: string): string {
    return this._serverUrl + `/audio/users/${userId}/videos/${videoId}`
  }

	public getGetAllUserAudioRecordingsUrl(userId: string): string {
    return this._serverUrl + `/audio/users/${userId}/recordings`
  }

	public getDeleteUserAudioRecordingUrl(userId: string, recordingId: string): string {
    return this._serverUrl + `/audio/users/${userId}/recordings/${recordingId}`
  }

	public getDownloadUserAudioRecordingUrl(userId: string, recordingId: string): string {
    return this._serverUrl + `/audio/users/${userId}/recordings/${recordingId}`
  }

}
