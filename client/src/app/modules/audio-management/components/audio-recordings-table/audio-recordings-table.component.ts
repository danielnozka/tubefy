import { Component } from '@angular/core';
import { Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AudioRecordingDeletionConfirmationDialogComponent } from '../audio-recording-deletion-confirmation-dialog/audio-recording-deletion-confirmation-dialog.component';
import { AudioRecordingDownloaderService } from '../../services/audio-recording-downloader.service';
import { AudioRecordingPlayerService } from '../../services/audio-recording-player.service';
import { IAudioRecordingDeletionData } from '../../models/audio-recording-deletion-data';
import { IAudioRecording } from '../../models/audio-recording';

@Component({
  selector: 'tubefy-audio-recordings-table',
  templateUrl: './audio-recordings-table.component.html',
  styleUrls: ['./audio-recordings-table.component.css']
})
export class AudioRecordingsTableComponent {

  @Input() public userId!: string;
  @Input() public audioRecordings: IAudioRecording[] = [];

  public audioRecordingsTableColumns: string[] = [
    'artist', 
    'title', 
    'size', 
    'codec', 
    'bit-rate',
    'options'
  ];

  constructor(
    private _audioRecordingDownloaderService: AudioRecordingDownloaderService,
    private _audioRecordingPlayerService: AudioRecordingPlayerService, 
    private _audioRecordingDeletionConfirmationDialog: MatDialog
  ) {}
  
  public playAudioRecording(audioRecording: IAudioRecording): void {
    this._audioRecordingPlayerService.updateAudioRecordingBeingPlayed(this.userId, audioRecording);
  }

  public downloadAudioRecording(audioRecording: IAudioRecording): void {
    this._audioRecordingDownloaderService.downloadAudioRecording(this.userId, audioRecording.id).subscribe({
      next: (response: Blob) => {
        let blob = new Blob([response], { type: 'application/octet-stream' });
        let fileUrl = window.URL.createObjectURL(blob);
        let fileLink = document.createElement('a');
        fileLink.href = fileUrl;
        fileLink.download = `${audioRecording.artist} - ${audioRecording.title}.${audioRecording.codec.toLowerCase()}`
        fileLink.click();
        window.URL.revokeObjectURL(fileUrl);
        fileLink.remove();
      },
      error: (error) => {
        console.error('An error occurred while downloading audio recording', error);
      }
    });
  }

  public deleteAudioRecording(recording: IAudioRecording): void {
    let audioRecordingDeletionData: IAudioRecordingDeletionData = {
      userId: this.userId,
      audioRecording: recording
    };
    this._audioRecordingDeletionConfirmationDialog.open(AudioRecordingDeletionConfirmationDialogComponent, {data: audioRecordingDeletionData});
  }

}
