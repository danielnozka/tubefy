import { Component } from '@angular/core';
import { Input } from '@angular/core';
import { OnDestroy } from '@angular/core';
import { AudioRecordingPlayerService } from '../../services/audio-recording-player.service';

@Component({
  selector: 'tubefy-audio-recording-player',
  templateUrl: './audio-recording-player.component.html',
  styleUrls: ['./audio-recording-player.component.css']
})
export class AudioRecordingPlayerComponent implements OnDestroy {

  @Input() public userId!: string;

  constructor(public audioRecordingPlayerService: AudioRecordingPlayerService) {}
  
  public playAudioRecording(): void {
    this.audioRecordingPlayerService.playAudioRecording();
  }

  public pauseAudioRecording(): void {
    this.audioRecordingPlayerService.pauseAudioRecording();
  }

  public playNextAudioRecording(): void {
    this.audioRecordingPlayerService.playNextAudioRecording(this.userId);
  }

  public playPreviousAudioRecording(): void {
    this.audioRecordingPlayerService.playPreviousAudioRecording(this.userId);
  }

  public ngOnDestroy(): void {
    this.pauseAudioRecording();
  }

}
