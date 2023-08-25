import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { IAudioRecordingSavingOptions } from './audio-recording-saving-options';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class AudioRecordingSavingService {

  private _audioRecordingSavingBaseUrl: string = environment.serverUrl + environment.endPoints.userAudioEndPoints.saveUserAudioRecordingEndPoint;

  constructor(private _httpClient: HttpClient) {}

  public saveAudioRecording(userId: string, videoId: string, audioRecordingSavingOptions: IAudioRecordingSavingOptions): Observable<Object> {
    let url = this._audioRecordingSavingBaseUrl.replace('{userId}', userId).replace('{videoId}', videoId);
    return this._httpClient.put(url, audioRecordingSavingOptions);
  }
    
}
