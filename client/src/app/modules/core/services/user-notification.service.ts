import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class UserNotificationService {
  
  private _snackBarsDurationMilliseconds: number = 5000.0;

  constructor(private _snackBar: MatSnackBar) {}

  public displaySuccessMessage(message: string): void {
    this._displayMessage(message, 'success-snack-bar');
  }

  public displayErrorMessage(message: string): void {
    this._displayMessage(message, 'error-snack-bar');
  }

  private _displayMessage(message: string, className: string): void {
    let snackBarOptions = {
      duration: this._snackBarsDurationMilliseconds,
      panelClass: [className]
    };
    this._snackBar.open(message, '', snackBarOptions);
  }

}
