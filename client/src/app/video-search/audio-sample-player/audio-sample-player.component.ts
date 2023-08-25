import { AudioRecordingSavingComponent } from './audio-recording-saving/audio-recording-saving.component';
import { AudioSamplePlayerService } from './audio-sample-player.service';
import { Component } from '@angular/core';
import { Input } from '@angular/core';
import { IVideoSearchResult } from '../video-search-result'
import { MatDialog } from '@angular/material/dialog';
import { OnDestroy } from '@angular/core';
import { OnInit } from '@angular/core';

@Component({
  selector: 'tubefy-audio-sample-player',
  templateUrl: './audio-sample-player.component.html',
  styleUrls: ['./audio-sample-player.component.css']
})
export class AudioSamplePlayerComponent implements OnInit, OnDestroy {

  @Input() public video!: IVideoSearchResult;
  public audioSample = new Audio();
  public audioSampleDuration: number = 0.0;
  public audioSampleCurrentTime: number = 0.0;
  public loadingAudioSample: boolean = false;

  constructor(private _audioSamplePlayerService: AudioSamplePlayerService, private _audioRecordingSavingMenu: MatDialog) {
    this.audioSample.addEventListener('timeupdate', () => {
      this.audioSampleCurrentTime = this.audioSample.currentTime;
    });
    this.audioSample.addEventListener('loadedmetadata', () => {
      this.audioSampleDuration = this.audioSample.duration;
    });
  }

  public openAudioRecordingSavingMenu() {
    this._audioRecordingSavingMenu.open(AudioRecordingSavingComponent, {data: this.video.videoId});
  }

  public async playAudioSample() : Promise<void> {
    this.loadingAudioSample = true;
    try {
      await this._audioSamplePlayerService.playAudioSample(this.video.videoId);
      if (this.audioSampleCurrentTime != 0.0) {
        this.audioSample.currentTime = this.audioSampleCurrentTime;
      }
    }
    catch (error) {
      console.error('An error occurred while getting audio samnple:', error)
    }
    this.loadingAudioSample = false;
  }

  public pauseAudioSample() : void {
    this._audioSamplePlayerService.pauseAudioSample(this.video.videoId);
  }

  public updateAudioSampleSliderPosition(position: number): void {
    this.audioSample.currentTime = position;
  }

  public ngOnInit(): void {
    this._audioSamplePlayerService.registerAudioSample(this.video.videoId, this.audioSample);
  }

  public ngOnDestroy(): void {
    this._audioSamplePlayerService.unregisterAudioSample(this.video.videoId);
  }

}
