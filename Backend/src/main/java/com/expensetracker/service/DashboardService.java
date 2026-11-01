
package com.expensetracker.service;

import com.expensetracker.dto.DashboardSummaryResponse;
import com.expensetracker.dto.RecentTransactionResponse;
import com.expensetracker.entity.User;
import com.expensetracker.repository.ExpenseRepository;
import com.expensetracker.repository.IncomeRepository;
import com.expensetracker.repository.UserRepository;

import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

@Service
public class DashboardService {

    private final ExpenseRepository expenseRepository;
    private final IncomeRepository incomeRepository;
    private final UserRepository userRepository;

    public DashboardService(
            ExpenseRepository expenseRepository,
            IncomeRepository incomeRepository,
            UserRepository userRepository
    ) {
        this.expenseRepository = expenseRepository;
        this.incomeRepository = incomeRepository;
        this.userRepository = userRepository;
    }

    public DashboardSummaryResponse getSummary() {

        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Long userId = user.getId();

        // Get total income and expenses directly from the database
        Double totalIncome =
                incomeRepository.getTotalIncomeByUserId(userId);

        Double totalExpense =
                expenseRepository.getTotalExpenseByUserId(userId);

        // Get category-wise expense totals
        Map<String, Double> categoryTotals = new LinkedHashMap<>();

        for (Object[] row :
                expenseRepository.getCategoryTotalsByUserId(userId)) {

            String category = (String) row[0];
            Double amount = ((Number) row[1]).doubleValue();

            categoryTotals.put(category, amount);
        }

        // Calculate balance
        Double balance = totalIncome - totalExpense;

        // Fetch only the 5 most recent expenses
        List<RecentTransactionResponse> recentExpenses =
                expenseRepository
                        .findTop5ByUser_IdOrderByDateDescIdDesc(userId)
                        .stream()
                        .map(expense -> new RecentTransactionResponse(
                                expense.getId(),
                                expense.getTitle(),
                                expense.getAmount(),
                                expense.getCategory(),
                                expense.getDate(),
                                "EXPENSE"
                        ))
                        .toList();

        // Fetch only the 5 most recent incomes
        List<RecentTransactionResponse> recentIncomes =
                incomeRepository
                        .findTop5ByUser_IdOrderByDateDescIdDesc(userId)
                        .stream()
                        .map(income -> new RecentTransactionResponse(
                                income.getId(),
                                income.getSource(),
                                income.getAmount(),
                                income.getCategory(),
                                income.getDate(),
                                "INCOME"
                        ))
                        .toList();

        // Combine both lists, sort by date, and keep the latest 5
        List<RecentTransactionResponse> recentTransactions =
                Stream.concat(
                                recentExpenses.stream(),
                                recentIncomes.stream()
                        )
                        .sorted(
                                Comparator.comparing(
                                        RecentTransactionResponse::date
                                ).reversed()
                        )
                        .limit(5)
                        .toList();

        // Count all transactions without loading them
        Long totalTransactions =
                expenseRepository.countByUser_Id(userId)
                        + incomeRepository.countByUser_Id(userId);

        return new DashboardSummaryResponse(
                totalIncome,
                totalExpense,
                balance,
                categoryTotals,
                recentTransactions,
                totalTransactions
        );
    }
}
