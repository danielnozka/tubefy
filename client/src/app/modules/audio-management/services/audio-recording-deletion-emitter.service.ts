import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AudioRecordingDeletionEmitterService {

  private _audioRecordingDeletedSource = new Subject<void>();
  public audioRecordingDeleted = this._audioRecordingDeletedSource.asObservable();

  public emit(): void {
    this._audioRecordingDeletedSource.next();
  }

}
