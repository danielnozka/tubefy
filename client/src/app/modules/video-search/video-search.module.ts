import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NgModule } from '@angular/core';
import { AudioRecordingSavingMenuComponent } from './components/audio-recording-saving-menu/audio-recording-saving-menu.component';
import { AudioSamplePlayerComponent } from './components/audio-sample-player/audio-sample-player.component';
import { VideoSearchResultsComponent } from './components/video-search-results-component/video-search-results.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatSliderModule,
    MatToolbarModule
  ],
  declarations: [
    AudioRecordingSavingMenuComponent,
    AudioSamplePlayerComponent,
    VideoSearchResultsComponent
  ],
  exports: [
    AudioRecordingSavingMenuComponent,
    AudioSamplePlayerComponent,
    VideoSearchResultsComponent
  ],
})
export class VideoSearchModule {}
