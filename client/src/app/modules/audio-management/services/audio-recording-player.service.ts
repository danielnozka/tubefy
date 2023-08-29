import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { IAudioRecording } from '../models/audio-recording';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class AudioRecordingPlayerService {
  
  public audio = new Audio();
  public audioDuration: number = 0.0;
  public audioCurrentTime: number = 0.0;
  public audioRecordingBeingPlayed!: IAudioRecording;
  private _audioRecordingsPlaylist: IAudioRecording[] = [];

  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {
    this.audio.addEventListener('timeupdate', () => {
      this.audioCurrentTime = this.audio.currentTime;
    });
    this.audio.addEventListener('loadedmetadata', () => {
      this.audioDuration = this.audio.duration;
    });
  }

  public playAudioRecording(): void {
    if (this.audioRecordingBeingPlayed) {
      this.audio.play();
    }
  }

  public pauseAudioRecording(): void {
    this.audio.pause();
  }

  public playNextAudioRecording(userId: string): void {
    if (this.audioRecordingBeingPlayed) {
      let currentIndex = this._audioRecordingsPlaylist.indexOf(this.audioRecordingBeingPlayed);
      if (currentIndex === -1) {
        console.error('Audio recording being played not found on the playlist');
      }
      else {
        let nextIndex = (currentIndex + 1) % this._audioRecordingsPlaylist.length;
        let nextAudioRecording = this._audioRecordingsPlaylist[nextIndex];
        this.updateAudioRecordingBeingPlayed(userId, nextAudioRecording);
      }
    }
  }

  public playPreviousAudioRecording(userId: string): void {
    if (this.audioRecordingBeingPlayed) {
      let currentIndex = this._audioRecordingsPlaylist.indexOf(this.audioRecordingBeingPlayed);
      if (currentIndex === -1) {
        console.error('Audio recording being played not found on the playlist');
      }
      else {
        let previousIndex = (currentIndex - 1 + this._audioRecordingsPlaylist.length) % this._audioRecordingsPlaylist.length;
        let previousAudioRecording = this._audioRecordingsPlaylist[previousIndex];
        this.updateAudioRecordingBeingPlayed(userId, previousAudioRecording);
      }
    }
  }

  public updateAudioRecordingBeingPlayed(userId: string, audioRecording: IAudioRecording): void {
    let url = this._serverConfigurationService.getPlayUserSavedAudioUrl(userId, audioRecording.id);
    this._httpClient.get(url, { responseType: 'blob' }).subscribe({
      next: (response: Blob) => {
        let audioBlob = new Blob([response], { type: 'audio/mpeg' });
        let audioUrl = URL.createObjectURL(audioBlob);
        this.audio.src = audioUrl;
        this.audio.play();
        this.audioRecordingBeingPlayed = audioRecording;
      },
      error: (error) => {
        console.log('An error occurred while getting audio recording:', error)
      }
    });
  }

  public updateAudioRecordingsPlaylist(audioRecordings: IAudioRecording[]): void {
    this._audioRecordingsPlaylist = audioRecordings;
  }

  public updateAudioCurrentTime(position: number): void {
    this.audio.currentTime = position;
  }
  
}
