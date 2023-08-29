import { IAudioRecording } from "./audio-recording";

export interface IAudioRecordingDeletionData {
  userId: string;
  audioRecording: IAudioRecording;
}
