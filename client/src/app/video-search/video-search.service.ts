import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { IVideoSearchResult } from './video-search-result';
import { Observable } from 'rxjs';

@Injectable()
export class VideoSearchService {
  
  private _searchVideosBaseUrl: string = environment.serverUrl + environment.endPoints.videoSearchEndPoints.searchVideosEndPoint;

  constructor(private _httpClient: HttpClient) {}

  public searchVideos(searchQuery: string): Observable<IVideoSearchResult[]> {
    let url = this._searchVideosBaseUrl.replace('{query}', encodeURIComponent(searchQuery));
    return this._httpClient.get<IVideoSearchResult[]>(url);
  }
  
}
