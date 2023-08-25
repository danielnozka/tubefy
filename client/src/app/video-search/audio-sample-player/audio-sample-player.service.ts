import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class AudioSamplePlayerService {

  private _playAudioSampleBaseUrl: string = environment.serverUrl + environment.endPoints.audioPlayerEndPoints.playAudioSampleEndPoint;
  private _audioSamples: { [videoId: string] : HTMLAudioElement } = {};
  private _videoIdAudioSampleBeingPlayed: string = '';

  constructor(private _httpClient: HttpClient) {}

  public registerAudioSample(videoId: string, audio: HTMLAudioElement): void {
    this._audioSamples[videoId] = audio;
  }

  public unregisterAudioSample(videoId: string): void {
    delete this._audioSamples[videoId];
  }

  public async playAudioSample(videoId: string): Promise<void> {
    if (this._videoIdAudioSampleBeingPlayed != '' && videoId != this._videoIdAudioSampleBeingPlayed) {
      this.pauseAudioSample(this._videoIdAudioSampleBeingPlayed);
    }
    if (videoId == this._videoIdAudioSampleBeingPlayed) {
      this._audioSamples[videoId].play();
    }
    else {
      try {
        await this._getAudioSample(videoId);
        this._videoIdAudioSampleBeingPlayed = videoId;
        this._audioSamples[videoId].play();
      }
      catch (error) {
        throw error;
      }
    }
  }

  public pauseAudioSample(videoId: string): void {
    this._audioSamples[videoId].pause();
  }

  private async _getAudioSample(videoId: string): Promise<void> {
    let url = this._playAudioSampleBaseUrl.replace('{videoId}', videoId);
    return new Promise<void>((resolve, reject) => {
      this._httpClient.get(url, { responseType: 'blob' }).subscribe({
        next: (blob) => {
          const audioBlob = new Blob([blob], { type: 'audio/mpeg' });
          const audioUrl = URL.createObjectURL(audioBlob);
          this._audioSamples[videoId].src = audioUrl;
          resolve();
        },
        error: (error) => {
          reject(error);
        }
      });
    });
  }
    
}
