import { Component, inject, PLATFORM_ID, OnInit } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-home',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {

  private authService = inject(AuthService);
  private platformId = inject(PLATFORM_ID);

  isLoggedIn = false;

  currentYear = new Date().getFullYear();

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.isLoggedIn = this.authService.isLoggedIn();
    }
  }
}