import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IAudioRecordingSavingOptions } from '../models/audio-recording-saving-options';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class AudioRecordingSavingService {

  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {}

  public saveAudioRecording(userId: string, videoId: string, audioRecordingSavingOptions: IAudioRecordingSavingOptions): Observable<Object> {
    let url = this._serverConfigurationService.getSaveUserAudioRecordingUrl(userId, videoId);
    return this._httpClient.put(url, audioRecordingSavingOptions);
  }
    
}
