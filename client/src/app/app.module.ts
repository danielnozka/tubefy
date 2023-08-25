import { AppComponent } from './app.component';
import { AudioManagementComponent } from './audio-management/audio-management.component';
import { AudioRecordingSavingComponent } from './video-search/audio-sample-player/audio-recording-saving/audio-recording-saving.component';
import { AudioSamplePlayerComponent } from './video-search/audio-sample-player/audio-sample-player.component';
import { AudioSamplePlayerService } from './video-search/audio-sample-player/audio-sample-player.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NgModule } from '@angular/core';
import { VideoSearchComponent } from './video-search/video-search.component';

@NgModule({
  declarations: [
    AppComponent,
    AudioManagementComponent,
    AudioRecordingSavingComponent,
    AudioSamplePlayerComponent,
    VideoSearchComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    HttpClientModule,
    MatButtonModule,
    MatCardModule,
    MatDialogModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatSliderModule,
    MatSnackBarModule,
    MatTableModule,
    MatToolbarModule
  ],
  providers: [AudioSamplePlayerService],
  bootstrap: [AppComponent]
})
export class AppModule {}
