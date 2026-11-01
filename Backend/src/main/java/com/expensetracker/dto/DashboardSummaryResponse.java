package com.expensetracker.dto;

import java.util.List;
import java.util.Map;

public record DashboardSummaryResponse(
        Double totalIncome,
        Double totalExpense,
        Double balance,
        Map<String, Double> categoryTotals,
        List<RecentTransactionResponse> recentTransactions,
        Long totalTransactions
) {}