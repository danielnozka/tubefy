import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IAudioRecording } from '../models/audio-recording';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class AudioRecordingsGetterService {
  
  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {}

  public getAudioRecordings(userId: string): Observable<IAudioRecording[]> {
    let url = this._serverConfigurationService.getGetAllUserAudioRecordingsUrl(userId);
    return this._httpClient.get<IAudioRecording[]>(url);
  }
  
}
