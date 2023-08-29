import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSliderModule } from '@angular/material/slider';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NgModule } from '@angular/core';
import { AudioRecordingDeletionConfirmationDialogComponent } from './components/audio-recording-deletion-confirmation-dialog/audio-recording-deletion-confirmation-dialog.component';
import { AudioRecordingPlayerComponent } from './components/audio-recording-player/audio-recording-player.component';
import { AudioRecordingResultsComponent } from './components/audio-recording-results/audio-recording-results.component';
import { AudioRecordingsTableComponent } from './components/audio-recordings-table/audio-recordings-table.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
    MatDividerModule,
    MatIconModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSliderModule,
    MatTableModule,
    MatToolbarModule
  ],
  declarations: [
    AudioRecordingDeletionConfirmationDialogComponent,
    AudioRecordingPlayerComponent,
    AudioRecordingResultsComponent,
    AudioRecordingsTableComponent
  ],
  exports: [
    AudioRecordingDeletionConfirmationDialogComponent,
    AudioRecordingPlayerComponent,
    AudioRecordingResultsComponent,
    AudioRecordingsTableComponent
  ],
})
export class AudioManagementModule {}
