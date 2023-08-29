import { Component } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatDialogRef } from '@angular/material/dialog';
import { AudioRecordingSavingService } from '../../services/audio-recording-saving.service';
import { IAudioRecordingSavingData } from '../../models/audio-recording-saving-data';
import { IAudioRecordingSavingOptions } from '../../models/audio-recording-saving-options';
import { UserNotificationService } from 'src/app/modules/core/services/user-notification.service';

@Component({
  selector: 'tubefy-audio-recording-saving-menu',
  templateUrl: './audio-recording-saving-menu.component.html',
  styleUrls: ['./audio-recording-saving-menu.component.css']
})
export class AudioRecordingSavingMenuComponent {

  public codecs: string[] = ['MP3', 'FLAC'];
  public bitRates: number[] = [192, 256, 320];
  public selectedTitle: string = '';
  public selectedArtist: string = '';
  public selectedCodec: string = 'MP3';
  public selectedBitRate: number = 320;
  public savingAudioRecording: boolean = false;
  private _userId: string;
  private _videoId: string;

  constructor(
    private _audioRecordingSavingService: AudioRecordingSavingService, 
    private _userNotificationService: UserNotificationService,
    @Inject(MAT_DIALOG_DATA) public audioRecordingSavingData: IAudioRecordingSavingData,
    private _matDialogRef: MatDialogRef<AudioRecordingSavingMenuComponent>
  ) {
    this._userId = audioRecordingSavingData.userId;
    this._videoId = audioRecordingSavingData.videoId;
  }

  public saveAudioRecording(): void {
    let audioRecordingSavingOptions: IAudioRecordingSavingOptions = {
      id: this._videoId,
      title: this.selectedTitle,
      artist: this.selectedArtist,
      codec: this.selectedCodec,
      bitRate: this.selectedBitRate
    };
    this.savingAudioRecording = true;
    this._audioRecordingSavingService.saveAudioRecording(this._userId, this._videoId, audioRecordingSavingOptions).subscribe({
      next: () => {
        this.savingAudioRecording = false;
        this._userNotificationService.displaySuccessMessage('Audio recording saved successfuly');
        this._matDialogRef.close()
      },
      error: (error: HttpErrorResponse) => {
        this.savingAudioRecording = false;
        if (error.status === 409) {
          this._userNotificationService.displayErrorMessage('Audio recording already saved');
        }
        else {
          let message = 'An unexpected error occurred while saving audio recording';
          console.error(message + ':', error);
          this._userNotificationService.displayErrorMessage(message);
        }
        this._matDialogRef.close()
      }
    });
  }

}
