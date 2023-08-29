import { Component } from '@angular/core';
import { Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { OnDestroy } from '@angular/core';
import { OnInit } from '@angular/core';
import { AudioRecordingSavingMenuComponent } from '../audio-recording-saving-menu/audio-recording-saving-menu.component';
import { AudioSamplePlayerService } from '../../services/audio-sample-player.service';
import { IAudioRecordingSavingData } from '../../models/audio-recording-saving-data';
import { IVideoSearchResult } from '../../models/video-search-result';

@Component({
  selector: 'tubefy-audio-sample-player',
  templateUrl: './audio-sample-player.component.html',
  styleUrls: ['./audio-sample-player.component.css']
})
export class AudioSamplePlayerComponent implements OnInit, OnDestroy {

  @Input() public userId!: string;
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
    let audioRecordingSavingData: IAudioRecordingSavingData = {
      userId: this.userId,
      videoId: this.video.videoId
    };
    this._audioRecordingSavingMenu.open(AudioRecordingSavingMenuComponent, {data: audioRecordingSavingData});
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
    this.pauseAudioSample();
    this._audioSamplePlayerService.unregisterAudioSample(this.video.videoId);
  }

}
