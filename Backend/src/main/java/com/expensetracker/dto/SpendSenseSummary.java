package com.expensetracker.dto;

import java.util.List;

public record SpendSenseSummary(
        double totalSpent,
        List<CategorySpending> categoryBreakdown,
        MonthlyComparison monthlyComparison,
        List<String> recommendations
) {
    public record CategorySpending(
            String category,
            double amount,
            double percentage
    ) {}

    public record MonthlyComparison(
            double currentMonthSpent,
            double previousMonthSpent,
            Double percentageChange
    ) {}
}