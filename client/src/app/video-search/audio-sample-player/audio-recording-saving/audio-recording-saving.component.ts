import { AudioRecordingSavingService } from './audio-recording-saving.service';
import { Component } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { IAudioRecordingSavingOptions } from './audio-recording-saving-options';
import { Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'tubefy-audio-recording-saving',
  templateUrl: './audio-recording-saving.component.html',
  styleUrls: ['./audio-recording-saving.component.css'],
  providers: [AudioRecordingSavingService]
})
export class AudioRecordingSavingComponent {

  public codecs: string[] = ['MP3', 'FLAC'];
  public bitRates: number[] = [192, 256, 320];
  public selectedTitle: string = 'Never gonna give you up';
  public selectedArtist: string = 'Rick Astley';
  public selectedCodec: string = 'MP3';
  public selectedBitRate: number = 320;
  public showProgressBar: boolean = false;
  private _userId: string = 'f42c756a-46a3-46a8-9af4-72e8cfeef685';
  private _snackBarsDurationMilliseconds: number = 5000.0;

  constructor(
    private _audioRecordingSavingService: AudioRecordingSavingService, 
    private _audioRecordingSavingSnackBar: MatSnackBar, 
    @Inject(MAT_DIALOG_DATA) private _videoId: string,
    private _matDialogRef: MatDialogRef<AudioRecordingSavingComponent>
  ) {}

  public saveAudioRecording(): void {
    let audioRecordingSavingOptions: IAudioRecordingSavingOptions = {
      id: this._videoId,
      title: this.selectedTitle,
      artist: this.selectedArtist,
      codec: this.selectedCodec,
      bitRate: this.selectedBitRate
    }
    this.showProgressBar = true;
    this._audioRecordingSavingService.saveAudioRecording(this._userId, this._videoId, audioRecordingSavingOptions).subscribe({
      next: () => {
        this.showProgressBar = false;
        this._showAudioRecordingSavingMessage('Audio recording saved successfully', 'success-snack-bar');
        this._matDialogRef.close()
      },
      error: (error: HttpErrorResponse) => {
        this.showProgressBar = false;
        if (error.status === 409) {
          this._showAudioRecordingSavingMessage('Audio recording already saved', 'error-snack-bar');
        }
        else {
          console.error('An unexpected error occurred while saving audio recording:', error);
          this._showAudioRecordingSavingMessage('An unexpected error occurred while saving audio recording', 'error-snack-bar');
        }
        this._matDialogRef.close()
      }
    });
  }

  private _showAudioRecordingSavingMessage(message: string, className: string): void {
    let snackBarOptions = {
      duration: this._snackBarsDurationMilliseconds,
      panelClass: [className]
    };
    this._audioRecordingSavingSnackBar.open(message, '', snackBarOptions);
  }

}
