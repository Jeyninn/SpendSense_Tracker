
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface SpendSensePrediction {
  is_anomaly: boolean;
  anomaly_score: number;
  severity: string;
  explanation: string;
  model_version: string;
}

export interface SpendSenseInsight {
  expenseId: number;
  title: string;
  amount: number;
  category: string;
  date: string;
  prediction: SpendSensePrediction;
}
export interface CategorySpending {
  category: string;
  amount: number;
  percentage: number;
}

export interface MonthlyComparison {
  currentMonthSpent: number;
  previousMonthSpent: number;
  percentageChange: number | null;
}

export interface SpendSenseSummary {
  totalSpent: number;
  categoryBreakdown: CategorySpending[];
  monthlyComparison: MonthlyComparison;
  recommendations: string[];
}

@Injectable({
  providedIn: 'root'
})
export class SpendSenseService {

  private http = inject(HttpClient);

  private apiUrl = `${environment.apiUrl}/api/spendsense`;

  getInsights(): Observable<SpendSenseInsight[]> {
    return this.http.get<SpendSenseInsight[]>(
      `${this.apiUrl}/insights`
    );
  }
  getSpendingSummary() {
  return this.http.get<SpendSenseSummary>(
    `${this.apiUrl}/summary`
  );
}
}
