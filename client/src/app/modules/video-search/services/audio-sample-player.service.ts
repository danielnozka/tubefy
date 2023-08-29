import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class AudioSamplePlayerService {

  private _audioSamples: { [videoId: string] : HTMLAudioElement } = {};
  private _videoIdAudioSampleBeingPlayed: string = '';

  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {}

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
    let url = this._serverConfigurationService.getPlayAudioSampleUrl(videoId);
    return new Promise<void>((resolve, reject) => {
      this._httpClient.get(url, { responseType: 'blob' }).subscribe({
        next: (response: Blob) => {
          let audioBlob = new Blob([response], { type: 'audio/mpeg' });
          let audioUrl = URL.createObjectURL(audioBlob);
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
