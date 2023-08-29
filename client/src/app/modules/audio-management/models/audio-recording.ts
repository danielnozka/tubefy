export interface IAudioRecording {
  id: string;
  videoId: string;
  title: string;
  artist: string;
  fileSizeMegabytes: number;
  codec: string;
  bitRate: number;
}
