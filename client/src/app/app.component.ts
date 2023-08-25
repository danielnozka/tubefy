import { Component} from '@angular/core';
import { VideoSearchComponent } from './video-search/video-search.component';
import { ViewChild } from '@angular/core';

@Component({
  selector: 'tubefy-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  public audioManagementEnabled: boolean = false;
  public videoSearchEnabled: boolean = true;
  public searchQuery: string = 'rick astley never gonna give you up';

  @ViewChild('videoSearchComponent') private _videoSearchComponent!: VideoSearchComponent;

  public showVideoSearchContent(): void {
    this.audioManagementEnabled = false;
    this.videoSearchEnabled = true;
  }

  public showAudioManagementContent(): void {
    this.audioManagementEnabled = true;
    this.videoSearchEnabled = false;
  }

  public searchVideos(): void {
    this._videoSearchComponent.searchVideos(this.searchQuery);
  }

}
