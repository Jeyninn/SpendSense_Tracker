
import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IncomeService } from '../../services/income';
import { Income } from '../../models/income.model';

@Component({
  selector: 'app-income-form',
  imports: [ReactiveFormsModule],
  templateUrl: './income-form.html',
  styleUrl: './income-form.css',
})
export class IncomeForm {

  private fb = inject(FormBuilder);
  private incomeService = inject(IncomeService);
  private router = inject(Router);

  loading = false;
  errorMessage = '';

  incomeForm = this.fb.group({
    source: ['', Validators.required],
    amount: [null as number | null, [Validators.required, Validators.min(1)]],
    category: ['', Validators.required],
    date: [new Date().toLocaleDateString('en-CA'), Validators.required],
    description: ['']
  });

  onSubmit() {

    if (this.incomeForm.invalid) {
      this.incomeForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    const income = this.incomeForm.getRawValue() as Income;

    this.incomeService.addIncome(income).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        console.error('Error adding income:', error);
        this.loading = false;
        this.errorMessage = 'Unable to save income. Please try again.';
      }
    });
  }

  cancel() {
    this.router.navigate(['/dashboard']);
  }
}
