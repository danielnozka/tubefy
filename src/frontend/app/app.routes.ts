import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/auth/login',
    pathMatch: 'full'
  },
  {
    path: 'auth',
    loadComponent: () => import('./layouts/authentication/authentication.component').then(
      m => m.AuthenticationComponent
    ),
    loadChildren: () => import('./features/authentication/authentication.routes').then(m => m.routes)
  },
  { 
    path: '**', 
    redirectTo: '/auth/login', 
    pathMatch: 'full' 
  }
];
