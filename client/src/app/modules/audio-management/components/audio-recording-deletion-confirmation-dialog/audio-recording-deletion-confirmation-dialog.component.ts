import { Component } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatDialogRef } from '@angular/material/dialog';
import { AudioRecordingDeletionEmitterService } from '../../services/audio-recording-deletion-emitter.service';
import { AudioRecordingDeleterService } from '../../services/audio-recording-deletter.service';
import { IAudioRecordingDeletionData } from '../../models/audio-recording-deletion-data';
import { IAudioRecording } from '../../models/audio-recording';
import { UserNotificationService } from 'src/app/modules/core/services/user-notification.service';

@Component({
  selector: 'tubefy-audio-recording-deletion-confirmation-dialog',
  templateUrl: './audio-recording-deletion-confirmation-dialog.component.html',
  styleUrls: ['./audio-recording-deletion-confirmation-dialog.component.css']
})
export class AudioRecordingDeletionConfirmationDialogComponent {

  public deletingAudioRecording: boolean = false;
  public audioRecording: IAudioRecording;
  private _userId: string;

  constructor(
    private _audioRecordingDeletionEmitterService: AudioRecordingDeletionEmitterService,
    private _audioRecordingDeleterService: AudioRecordingDeleterService, 
    private _userNotificationService: UserNotificationService,
    @Inject(MAT_DIALOG_DATA) public audioRecordingDeletionData: IAudioRecordingDeletionData,
    private _matDialogRef: MatDialogRef<AudioRecordingDeletionConfirmationDialogComponent>
  ) {
    this.audioRecording = audioRecordingDeletionData.audioRecording;
    this._userId = audioRecordingDeletionData.userId;
  }

  public deleteAudioRecording(): void {
    this.deletingAudioRecording = true;
    this._audioRecordingDeleterService.deleteAudioRecording(this._userId, this.audioRecording.id).subscribe({
      next: () => {
        this.deletingAudioRecording = false;
        this._userNotificationService.displaySuccessMessage('Audio recording removed successfuly');
        this._matDialogRef.close()
        this._audioRecordingDeletionEmitterService.emit();
      },
      error: (error: HttpErrorResponse) => {
        this.deletingAudioRecording = false;
        let message = 'An unexpected error occurred while deleting audio recording';
        console.error(message + ':', error);
        this._userNotificationService.displayErrorMessage(message);
        this._matDialogRef.close()
      }
    });
  }

}
