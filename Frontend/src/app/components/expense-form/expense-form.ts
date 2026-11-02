import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Expense } from '../../models/expense.model';
import { ExpenseService } from '../../services/expense';

@Component({
  selector: 'app-expense-form',
  imports: [ReactiveFormsModule],
  templateUrl: './expense-form.html',
  styleUrl: './expense-form.css',
})
export class ExpenseForm {

  private fb = inject(FormBuilder);
  private expenseService = inject(ExpenseService);
  private router = inject(Router);

  expenseForm = this.fb.group({
    title: ['', Validators.required],
    amount: [0, [Validators.required, Validators.min(1)]],
    category: ['', Validators.required],
    date: ['', Validators.required],
    description: [''],
  });

  submit(): void {

    if (this.expenseForm.invalid) {
      this.expenseForm.markAllAsTouched();
      return;
    }

    const formValue = this.expenseForm.getRawValue();

    const expense: Expense = {
      title: formValue.title!,
      amount: Number(formValue.amount),
      category: formValue.category!,
      date: formValue.date!,
      description: formValue.description ?? ''
    };

    this.expenseService.addExpense(expense).subscribe({

      next: (savedExpense) => {

        console.log('Expense saved:', savedExpense);

        // Go back to dashboard after successful POST
        this.router.navigate(['/dashboard']);

      },

      error: (error) => {
        console.error('Error saving expense:', error);
      }

    });
  }
}