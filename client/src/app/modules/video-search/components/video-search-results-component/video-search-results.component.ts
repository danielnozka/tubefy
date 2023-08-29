import { Component } from '@angular/core';
import { Input } from '@angular/core';
import { IVideoSearchResult } from '../../models/video-search-result';
import { VideoSearchService } from '../../services/video-search.service';

@Component({
  selector: 'tubefy-video-search-results',
  templateUrl: './video-search-results.component.html',
  styleUrls: ['./video-search-results.component.css']
})
export class VideoSearchResultsComponent {

  @Input() public userId!: string;
  public videoSearchResults: IVideoSearchResult[] = [];
  public noResultsContent: string = 'Complete the search field to start looking for videos';
  public searchingVideos: boolean = false;

  constructor(private _videoSearchService: VideoSearchService) {}

  public searchVideos(message: string): void {
    this.videoSearchResults = [];
    this.searchingVideos = true;
    this._videoSearchService.searchVideos(message).subscribe({
      next: (response) => {
        this.searchingVideos = false;
        this.videoSearchResults = response;
      },
      error: (error) => {
        console.error('An error occurred while searching for videos', error);
        this.searchingVideos = false;
        this.noResultsContent = 'An error occurred while searching for videos';
      }
    });
  }

}
