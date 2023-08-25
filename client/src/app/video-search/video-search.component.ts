import { Component } from '@angular/core';
import { IVideoSearchResult } from './video-search-result';
import { VideoSearchService } from './video-search.service';

@Component({
  selector: 'tubefy-video-search',
  templateUrl: './video-search.component.html',
  styleUrls: ['./video-search.component.css'],
  providers: [
    VideoSearchService
  ]
})
export class VideoSearchComponent {

  public videoSearchResult: IVideoSearchResult[] = [];
  public noResultsContent: string = 'Complete the search field to start looking for videos';
  public searchingVideos: boolean = false;

  constructor(private _videoSearchService: VideoSearchService) {}

  public searchVideos(message: string): void {
    this.videoSearchResult = [];
    this.searchingVideos = true;
    this._videoSearchService.searchVideos(message).subscribe({
      next: (response) => {
        this.searchingVideos = false;
        this.videoSearchResult = response;
      },
      error: (error) => {
        console.error('An error occurred while searching for videos', error);
        this.searchingVideos = false;
        this.noResultsContent = 'An error occurred while searching for videos';
      }
    });
  }

}
