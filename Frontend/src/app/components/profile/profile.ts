import { Component, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router ,RouterLink} from '@angular/router';
import { AuthService } from '../../services/auth';
@Component({
  selector: 'app-profile',
  imports: [RouterLink],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class Profile {
  private platformId = inject(PLATFORM_ID);
  private auth=inject(AuthService)
  private router = inject(Router);
  userName = 'Guest';
  userEmail = 'No email';
  userInitial = 'G';

  ngOnInit() {
    this.loadUser();
  }
  loadUser() {

    if (!isPlatformBrowser(this.platformId)) {
      return;
    }

    const user = localStorage.getItem('user');

    if (!user) {
      return;
    }

    const userData = JSON.parse(user);

    this.userName = userData.name;
    this.userEmail = userData.email;

    this.userInitial = userData.name
      .charAt(0)
      .toUpperCase();
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}






