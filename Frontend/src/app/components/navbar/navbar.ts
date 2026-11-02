import { Component, PLATFORM_ID, inject, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit {

  private platformId = inject(PLATFORM_ID);

  userName = 'Guest';
  userInitial = 'G';
  userEmail = '';

  ngOnInit() {
    this.loadUser();
  }

  loadUser() {
    if (!isPlatformBrowser(this.platformId)) return;

    const user = localStorage.getItem('user');

    if (user) {
      const userData = JSON.parse(user);

      this.userName = userData.name || 'Guest';
      this.userEmail = userData.email || '';
      this.userInitial = this.userName.charAt(0).toUpperCase();
    }
  }
}