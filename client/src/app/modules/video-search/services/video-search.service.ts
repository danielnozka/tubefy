import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IVideoSearchResult } from '../models/video-search-result';
import { ServerConfigurationService } from '../../core/services/server-configuration.service';

@Injectable({
  providedIn: 'root',
})
export class VideoSearchService {
  
  constructor(private _serverConfigurationService: ServerConfigurationService, private _httpClient: HttpClient) {}

  public searchVideos(searchQuery: string): Observable<IVideoSearchResult[]> {
    let url = this._serverConfigurationService.getSearchVideosUrl(searchQuery);
    return this._httpClient.get<IVideoSearchResult[]>(url);
  }
  
}
