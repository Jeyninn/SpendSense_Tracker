
import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule,RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {

  private fb = inject(FormBuilder);
  private router = inject(Router);
  private authService = inject(AuthService);

  loginform = this.fb.nonNullable.group({
  email: ['', [Validators.required, Validators.email]],
  password: ['', [Validators.required, Validators.minLength(6)]],
});

  loginAcc() {

    if (this.loginform.invalid) {
      this.loginform.markAllAsTouched();
      return;
    }

    const { email, password } = this.loginform.getRawValue();

    this.authService.login({
      email,
      password
    }).subscribe({
      next: (response) => {
        alert('Login successful!');
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        console.error(error);
        alert(error.error?.message || 'Invalid email or password!');
      }
    });
  }
}
