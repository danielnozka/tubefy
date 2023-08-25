import {Component} from '@angular/core';

@Component({
  selector: 'ytam-audio',
  templateUrl: './audio-management.component.html',
  styleUrls: ['./audio-management.component.css']
})
export class AudioManagementComponent {
  audioColumns: string[] = [
    'artist', 
    'title', 
    'size', 
    'codec', 
    'bitRate',
    'delete'
  ];
  audioResult: any[] = [
    {
      "artist": "Rick Astley",
      "title": "Never gonna give you up",
      "size": 9.81,
      "codec": "MP3",
      "bitRate": 320
    },
    {
      "artist": "Rick Astley",
      "title": "Never gonna give you up",
      "size": 9.81,
      "codec": "MP3",
      "bitRate": 320
    },
    {
      "artist": "Rick Astley",
      "title": "Never gonna give you up",
      "size": 9.81,
      "codec": "MP3",
      "bitRate": 320
    }
  ]
}
