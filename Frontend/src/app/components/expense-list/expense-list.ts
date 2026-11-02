
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { Expense } from '../../models/expense.model';
import { ExpenseService } from '../../services/expense';

@Component({
  selector: 'app-expense-list',
  imports: [],
  templateUrl: './expense-list.html',
  styleUrl: './expense-list.css',
})
export class ExpenseList implements OnInit {

  expenses: Expense[] = [];

  currentPage = 0;
  pageSize = 10;
  totalPages = 0;
  totalElements = 0;

  loading = false;
  errorMessage = '';

  private expenseService = inject(ExpenseService);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit() {
    this.loadExpenses();
  }

  loadExpenses() {
    this.loading = true;
    this.errorMessage = '';

    this.expenseService
      .getExpensesPage(this.currentPage, this.pageSize)
      .subscribe({
        next: (response) => {
          this.expenses = response.content;
          this.totalPages = response.totalPages;
          this.totalElements = response.totalElements;

          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (error) => {
          console.error('Error loading expenses:', error);

          this.loading = false;
          this.errorMessage =
            'Unable to load transactions. Please try again.';

          this.cdr.detectChanges();
        },
      });
  }

  nextPage() {
    if (this.currentPage < this.totalPages - 1) {
      this.currentPage++;
      this.loadExpenses();
    }
  }

  previousPage() {
    if (this.currentPage > 0) {
      this.currentPage--;
      this.loadExpenses();
    }
  }

  deleteExpense(id: number) {
    this.expenseService.deleteExpense(id).subscribe({
      next: () => {
        if (this.expenses.length === 1 && this.currentPage > 0) {
          this.currentPage--;
        }

        this.loadExpenses();
      },
      error: (error) => {
        console.error('Error deleting expense:', error);
      },
    });
  }

  get startRecord(): number {
    return this.totalElements === 0
      ? 0
      : this.currentPage * this.pageSize + 1;
  }

  get endRecord(): number {
    return Math.min(
      (this.currentPage + 1) * this.pageSize,
      this.totalElements
    );
  }
}
