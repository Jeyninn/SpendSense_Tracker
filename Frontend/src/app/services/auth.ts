
import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

interface AuthResponse {
  token: string;
  email: string;
  name: string;
}

interface SignupRequest {
  name: string;
  email: string;
  password: string;
}

interface LoginRequest {
  email: string;
  password: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID);

  private apiUrl = `${environment.apiUrl}/api/auth`;


  private saveUserData(response: AuthResponse) {
  if (isPlatformBrowser(this.platformId)) {
    localStorage.setItem('token', response.token);

    localStorage.setItem('user', JSON.stringify({
      name: response.name,
      email: response.email
    }));
  }
}
  signup(data: SignupRequest): Observable<AuthResponse> {
  return this.http.post<AuthResponse>(
    `${this.apiUrl}/register`, data
  ).pipe(
    tap(response => this.saveUserData(response))
  );
}

login(data: LoginRequest): Observable<AuthResponse> {
  return this.http.post<AuthResponse>(
    `${this.apiUrl}/login`, data
  ).pipe(
    tap(response => this.saveUserData(response))
  );
}

  getToken(): string | null {
    return isPlatformBrowser(this.platformId)
      ? localStorage.getItem('token')
      : null;
  }

  logout() {
  if (isPlatformBrowser(this.platformId)) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
}

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
