import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class AudioRecordingDeleterService {
  
  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {}

  public deleteAudioRecording(userId: string, recordingId: string): Observable<Object> {
    let url = this._serverConfigurationService.getDeleteUserAudioRecordingUrl(userId, recordingId);
    return this._httpClient.delete(url);
  }
  
}
