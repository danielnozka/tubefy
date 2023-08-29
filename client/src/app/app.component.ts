import { Component} from '@angular/core';
import { MatButton } from '@angular/material/button';
import { ViewChild } from '@angular/core';
import { VideoSearchResultsComponent } from './modules/video-search/components/video-search-results-component/video-search-results.component';

@Component({
  selector: 'tubefy-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  public showAudioRecordingResultsComponent: boolean = false;
  public showVideoSearchResultsComponent: boolean = true;
  public searchQuery: string = '';
  public userId: string = 'f42c756a-46a3-46a8-9af4-72e8cfeef685';
  private _videoSearchComponentSearchQuery: string = '';
  private _audioManagementFilterQuery: string = '';

  @ViewChild('searchButton') public searchButton!: MatButton;
  @ViewChild(VideoSearchResultsComponent) private _videoSearchResultsComponent!: VideoSearchResultsComponent;

  public showVideoSearchResultsComponentContent(): void {
    this._audioManagementFilterQuery = this.searchQuery;
    this.searchQuery = this._videoSearchComponentSearchQuery;
    this.showAudioRecordingResultsComponent = false;
    this.showVideoSearchResultsComponent = true;
  }

  public showAudioRecordingResultsComponentContent(): void {
    this._videoSearchComponentSearchQuery = this.searchQuery;
    this.searchQuery = this._audioManagementFilterQuery;
    this.showAudioRecordingResultsComponent = true;
    this.showVideoSearchResultsComponent = false;
  }

  public searchVideos(): void {
    this._videoSearchResultsComponent.searchVideos(this.searchQuery);
  }

}
