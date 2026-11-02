
import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-signup',
  imports: [ReactiveFormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.css',
})
export class Signup {

  private fb = inject(FormBuilder);
  private router = inject(Router);
  private authService = inject(AuthService);

  signupForm = this.fb.nonNullable.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    confirmPassword: ['', Validators.required]
  });

  createAccount() {

    if (this.signupForm.invalid) {
      this.signupForm.markAllAsTouched();
      return;
    }

    const { name, email, password, confirmPassword } =
      this.signupForm.getRawValue();

    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    const user = {
      name,
      email,
      password
    };

    this.authService.signup(user).subscribe({
      next: (response) => {
        alert('Account created successfully!');
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        console.error(error);
        alert(error.error?.message || 'Signup failed. Please try again.');
      }
    });
  }
}
