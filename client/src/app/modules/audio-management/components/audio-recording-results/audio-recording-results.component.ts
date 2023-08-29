import { Component } from '@angular/core';
import { Input } from '@angular/core';
import { OnInit } from '@angular/core';
import { AudioRecordingDeletionEmitterService } from '../../services/audio-recording-deletion-emitter.service';
import { AudioRecordingsGetterService } from '../../services/audio-recordings-getter.service';
import { AudioRecordingPlayerService } from '../../services/audio-recording-player.service';
import { IAudioRecording } from '../../models/audio-recording';

@Component({
  selector: 'tubefy-audio-recording-results',
  templateUrl: './audio-recording-results.component.html',
  styleUrls: ['./audio-recording-results.component.css']
})
export class AudioRecordingResultsComponent implements OnInit {

  @Input() public userId!: string;
  public audioRecordings: IAudioRecording[] = [];
  public filteredAudioRecordings: IAudioRecording[] = [];
  public gettingAudioRecordings: boolean = false;
  public noResultsContent: string = '';

  constructor(
    private _audioRecordingDeletionEmitterService: AudioRecordingDeletionEmitterService, 
    private _audioRecordingsGetterService: AudioRecordingsGetterService,
    private _audioRecordingPlayerService: AudioRecordingPlayerService
  ) {
    this._audioRecordingDeletionEmitterService.audioRecordingDeleted.subscribe(() => {
      this._getAudioRecordings();
    })
  }

  @Input() set audioRecordingsFilter(audioRecordingsFilter: string) {
    this.filteredAudioRecordings = this._filterAudioRecordings(audioRecordingsFilter);
  }

  public ngOnInit(): void {
    this._getAudioRecordings();
  }

  private _getAudioRecordings(): void {
    this.gettingAudioRecordings = true;
    this._audioRecordingsGetterService.getAudioRecordings(this.userId).subscribe({
      next: (response) => {
        this.gettingAudioRecordings = false;
        this.audioRecordings = response;
        this.filteredAudioRecordings = response;
        this._audioRecordingPlayerService.updateAudioRecordingsPlaylist(response);
        if (!this.audioRecordings.length) {
          this.noResultsContent = 'No audio recordings found';
        }
        else {
          this.noResultsContent = '';
        }
      },
      error: (error) => {
        console.error('An error occurred while getting audio recordings:', error);
        this.gettingAudioRecordings = false;
        this.noResultsContent = 'An error occurred while getting audio recordings';
      }
    });
  }

  private _filterAudioRecordings(audioRecordingsFilter: string): IAudioRecording[] {
    audioRecordingsFilter = audioRecordingsFilter.toLocaleLowerCase();
    return this.audioRecordings.filter((audioRecording: IAudioRecording) => 
      audioRecording.artist.toLocaleLowerCase().includes(audioRecordingsFilter) || audioRecording.title.toLocaleLowerCase().includes(audioRecordingsFilter));
  }

}
