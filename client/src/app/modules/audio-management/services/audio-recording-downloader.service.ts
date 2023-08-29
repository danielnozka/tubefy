import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class AudioRecordingDownloaderService {
  
  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {}

  public downloadAudioRecording(userId: string, recordingId: string): Observable<Blob> {
    let url = this._serverConfigurationService.getDownloadUserAudioRecordingUrl(userId, recordingId);
    return this._httpClient.get(url, {
      responseType: 'blob',
      headers: new HttpHeaders().append('Content-Type', 'application/octet-stream')
    });
  }

}
