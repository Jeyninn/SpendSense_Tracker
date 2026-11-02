
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Expense } from '../models/expense.model';
import { AuthService } from './auth';
import { environment } from '../../environments/environment';

export interface ExpensePage {
  content: Expense[];
  totalElements: number;
  totalPages: number;
  number: number;
  size: number;
  first: boolean;
  last: boolean;
  empty: boolean;
}

export interface RecentTransaction {
  id: number;
  title: string;
  amount: number;
  category: string;
  date: string;
  type: 'EXPENSE' | 'INCOME';
}

export interface DashboardSummary {
  totalIncome: number;
  totalExpense: number;
  balance: number;
  categoryTotals: Record<string, number>;
  recentTransactions: RecentTransaction[];
  totalTransactions: number;
}
@Injectable({
  providedIn: 'root'
})

export class ExpenseService {

  private http = inject(HttpClient);
  private auth = inject(AuthService);

  private apiUrl = `${environment.apiUrl}/api/expenses`;
  private dashboardUrl = `${environment.apiUrl}/api/dashboard`;

  private getHeaders() {
  const token = this.auth.getToken();

    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }
  getExpensesPage(page: number, size: number) {
  return this.http.get<ExpensePage>(
    `${this.apiUrl}/page`,
    {
      params: { page, size }
    }
  );
}
  getExpenses(): Observable<Expense[]> {
    return this.http.get<Expense[]>(this.apiUrl, {
      headers: this.getHeaders()
    });
  }

  addExpense(expense: Expense): Observable<Expense> {
    return this.http.post<Expense>(this.apiUrl, expense, {
      headers: this.getHeaders()
    });
  }

  deleteExpense(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, {
      headers: this.getHeaders()
    });
  }

  updateExpense(id: number, expense: Expense): Observable<Expense> {
    return this.http.put<Expense>(
      `${this.apiUrl}/${id}`,
      expense,
      { headers: this.getHeaders() }
    );
  }
  getDashboardSummary(): Observable<DashboardSummary> {
  return this.http.get<DashboardSummary>(
    `${this.dashboardUrl}/summary`,
    {
      headers: this.getHeaders()
    }
  );
}
}
