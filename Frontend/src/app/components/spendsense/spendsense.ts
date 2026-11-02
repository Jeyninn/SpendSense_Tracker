
import {
  Component,
  OnInit,
  OnDestroy,
  inject,
  ChangeDetectorRef,
  ElementRef,
  ViewChild
} from '@angular/core';

import { TitleCasePipe } from '@angular/common';

import {
  SpendSenseService,
  SpendSenseInsight,
  SpendSenseSummary
} from '../../services/spendsense';

import { forkJoin } from 'rxjs';

import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-spendsense',
  standalone: true,
  imports: [TitleCasePipe],
  templateUrl: './spendsense.html',
  styleUrl: './spendsense.css'
})
export class SpendSense implements OnInit, OnDestroy {

  private spendSenseService = inject(SpendSenseService);
  private cdr = inject(ChangeDetectorRef);

  insights: SpendSenseInsight[] = [];
  summary: SpendSenseSummary | null = null;

  loading = true;
  error = '';

  private categoryChart?: Chart;

  // Detect when the chart canvas appears in the HTML
  @ViewChild('categoryChart')
  set categoryChartCanvas(
    ref: ElementRef<HTMLCanvasElement> | undefined
  ) {
    if (ref && this.summary) {
      this.renderCategoryChart(ref.nativeElement);
    }
  }

  ngOnInit(): void {
    this.loadInsights();
  }

  // Fetch ML insights and monthly summary together
  loadInsights(): void {

    this.loading = true;
    this.error = '';

    forkJoin({
      insights: this.spendSenseService.getInsights(),
      summary: this.spendSenseService.getSpendingSummary()
    }).subscribe({

      next: (data) => {

        console.log('SpendSense insights:', data.insights);
        console.log('SpendSense summary:', data.summary);

        this.insights = data.insights;
        this.summary = data.summary;

        this.loading = false;

        this.cdr.markForCheck();
      },

      error: (err) => {

        console.error('SpendSense API error:', err);

        this.error = 'Unable to load spending insights.';
        this.loading = false;

        this.cdr.markForCheck();
      }
    });
  }

  // Render category-wise doughnut chart
  renderCategoryChart(canvas: HTMLCanvasElement): void {

    this.categoryChart?.destroy();

    if (!this.summary || this.summary.categoryBreakdown.length === 0) {
      return;
    }

    this.categoryChart = new Chart(canvas, {

      type: 'doughnut',

      data: {

        labels: this.summary.categoryBreakdown.map(
          item => item.category
        ),

        datasets: [{
          data: this.summary.categoryBreakdown.map(
            item => item.amount
          ),

          backgroundColor: [
            '#765438',
            '#B18B60',
            '#C9B99E',
            '#8B9278',
            '#D8C7AD'
          ],

          borderWidth: 3,
          borderColor: '#FAF7F1',
          hoverOffset: 8
        }]
      },

      options: {

        responsive: true,
        maintainAspectRatio: true,
        cutout: '72%',

        plugins: {

          legend: {
            display: false
          },

          tooltip: {
            callbacks: {
              label: (context) =>
                ` ₹${Number(context.raw).toFixed(2)}`
            }
          }
        }
      }
    });
  }

  // Number of unusual transactions
  get anomalyCount(): number {
    return this.insights.filter(
      item => item.prediction.is_anomaly
    ).length;
  }

  // High severity transactions
  get highCount(): number {
    return this.insights.filter(
      item => item.prediction.severity === 'high'
    ).length;
  }

  // Medium severity transactions
  get mediumCount(): number {
    return this.insights.filter(
      item => item.prediction.severity === 'medium'
    ).length;
  }

  // Normal transactions
  get normalCount(): number {
    return this.insights.filter(
      item => !item.prediction.is_anomaly
    ).length;
  }

  // Only flagged transactions
  get flaggedInsights(): SpendSenseInsight[] {
    return this.insights.filter(
      item => item.prediction.is_anomaly
    );
  }

  // Clean up chart when component is destroyed
  ngOnDestroy(): void {
    this.categoryChart?.destroy();
  }
}
