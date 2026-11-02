import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink, NavigationEnd } from '@angular/router';
import { NgClass, DecimalPipe } from '@angular/common';
import { filter } from 'rxjs';
import { ExpenseService, DashboardSummary } from '../../services/expense';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink, NgClass, DecimalPipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {

  private expenseService = inject(ExpenseService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  totalIncome = 0;
  totalExpense = 0;
  balance = 0;
  totalTransactions = 0;

  categoryEntries: { category: string; amount: number }[] = [];
  recentTransactions: DashboardSummary['recentTransactions'] = [];

  ngOnInit(): void {
    this.loadDashboardSummary();

    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        if (this.router.url === '/') {
          this.loadDashboardSummary();
        }
      });
  }

  loadDashboardSummary(): void {
    this.expenseService.getDashboardSummary().subscribe({
      next: summary => {
        this.totalIncome = summary.totalIncome;
        this.totalExpense = summary.totalExpense;
        this.balance = summary.balance;
        this.totalTransactions = summary.totalTransactions;
        this.recentTransactions = summary.recentTransactions;

        const normalizedTotals = new Map<string, number>();

        Object.entries(summary.categoryTotals).forEach(([category, amount]) => {
          const key = category.trim().toLowerCase();
          normalizedTotals.set(
            key,
            (normalizedTotals.get(key) ?? 0) + Number(amount)
          );
        });

        this.categoryEntries = Array.from(normalizedTotals.entries())
          .map(([category, amount]) => ({
            category: category.charAt(0).toUpperCase() + category.slice(1),
            amount
          }));

        this.cdr.detectChanges();
      },
      error: error => console.error('Error loading dashboard:', error)
    });
  }
}