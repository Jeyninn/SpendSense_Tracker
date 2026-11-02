
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Income } from '../models/income.model';
import { AuthService } from './auth';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class IncomeService {

  private http = inject(HttpClient);
  private auth = inject(AuthService);

  private apiUrl = `${environment.apiUrl}/api/incomes`;

  private getHeaders() {
  const token = this.auth.getToken();

    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }

  getIncomes(): Observable<Income[]> {
    return this.http.get<Income[]>(this.apiUrl, {
      headers: this.getHeaders()
    });
  }

  addIncome(income: Income): Observable<Income> {
    return this.http.post<Income>(this.apiUrl, income, {
      headers: this.getHeaders()
    });
  }

  updateIncome(id: number, income: Income): Observable<Income> {
    return this.http.put<Income>(
      `${this.apiUrl}/${id}`,
      income,
      { headers: this.getHeaders() }
    );
  }

  deleteIncome(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/${id}`,
      { headers: this.getHeaders() }
    );
  }
}
