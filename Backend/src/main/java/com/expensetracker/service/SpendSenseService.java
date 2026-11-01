package com.expensetracker.service;

import com.expensetracker.dto.SpendSenseInsight;
import com.expensetracker.dto.SpendSenseRequest;
import com.expensetracker.dto.SpendSenseResponse;
import com.expensetracker.entity.Expense;
import com.expensetracker.repository.ExpenseRepository;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;
import com.expensetracker.dto.SpendSenseSummary;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.ZoneId;
import java.util.LinkedHashMap;
import java.util.Map;
@Service
public class SpendSenseService {

    private final ExpenseRepository expenseRepository;
    private final RestClient restClient;

    public SpendSenseService(
            ExpenseRepository expenseRepository,
            @Value("${spendsense.api.url}") String apiUrl
    ) {
        this.expenseRepository = expenseRepository;
        this.restClient = RestClient.builder()
                .baseUrl(apiUrl)
                .build();
    }

    public List<SpendSenseInsight> analyzeExpenses(Long userId) {

        List<Expense> expenses =
                expenseRepository.findAllByUser_IdOrderByDateAscIdAsc(userId);

        List<SpendSenseInsight> insights = new ArrayList<>();

        for (int i = 0; i < expenses.size(); i++) {

            Expense expense = expenses.get(i);

            // Only consider transactions before the current expense.
            List<Expense> previousExpenses =
                    expenses.subList(0, i);

            // Find previous transactions in the same category.
            List<Double> categoryAmounts = previousExpenses.stream()
                    .filter(e -> e.getCategory() != null
                            && e.getCategory().equalsIgnoreCase(expense.getCategory()))
                    .map(Expense::getAmount)
                    .filter(amount -> amount != null && amount > 0)
                    .toList();

            // Use category history first, otherwise all previous expenses.
            List<Double> referenceAmounts = categoryAmounts.isEmpty()
                    ? previousExpenses.stream()
                    .map(Expense::getAmount)
                    .filter(amount -> amount != null && amount > 0)
                    .toList()
                    : categoryAmounts;

            boolean hasPersonalHistory = previousExpenses.size() >= 5;

            // Skip transactions without enough personal history.
            if (!hasPersonalHistory || referenceAmounts.isEmpty()) {
                continue;
            }

            double referenceAmount = calculateMedian(referenceAmounts);

            if (referenceAmount <= 0) {
                continue;
            }

            // Expense entity stores only LocalDate, not transaction time.
            int hour = 12;

            int dayOfWeek = expense.getDate()
                    .getDayOfWeek()
                    .getValue() - 1;

            SpendSenseRequest request = new SpendSenseRequest(
                    expense.getAmount(),
                    expense.getCategory(),
                    hour,
                    dayOfWeek,
                    referenceAmount,
                    true
            );

            SpendSenseResponse prediction = restClient.post()
                    .uri("/predict")
                    .body(request)
                    .retrieve()
                    .body(SpendSenseResponse.class);

            if (prediction != null) {
                insights.add(new SpendSenseInsight(
                        expense.getId(),
                        expense.getTitle(),
                        expense.getAmount(),
                        expense.getCategory(),
                        expense.getDate(),
                        prediction
                ));
            }
        }

        return insights;
    }

    private double calculateMedian(List<Double> values) {

        List<Double> sorted = values.stream()
                .sorted()
                .toList();

        int size = sorted.size();

        if (size == 0) {
            return 0;
        }

        if (size % 2 == 0) {
            return (sorted.get(size / 2 - 1)
                    + sorted.get(size / 2)) / 2.0;
        }

        return sorted.get(size / 2);
    }

    public SpendSenseSummary getSpendingSummary(Long userId) {

        List<Expense> expenses =
                expenseRepository.findAllByUser_IdOrderByDateAscIdAsc(userId);

        YearMonth currentMonth =
                YearMonth.now(ZoneId.of("Asia/Kolkata"));

        YearMonth previousMonth = currentMonth.minusMonths(1);

        double currentMonthTotal = 0;

        double previousMonthTotal = 0;

        Map<String, Double> categoryTotals = new LinkedHashMap<>();

        for (Expense expense : expenses) {

            if (expense.getDate() == null || expense.getAmount() == null
                    || expense.getAmount() <= 0) {
                continue;
            }

            YearMonth expenseMonth = YearMonth.from(expense.getDate());

            if (expenseMonth.equals(currentMonth)) {

                currentMonthTotal += expense.getAmount();

                String category = expense.getCategory();

                if (category == null || category.isBlank()) {
                    category = "other";
                }

                categoryTotals.merge(
                        category.toLowerCase(),
                        expense.getAmount(),
                        Double::sum
                );

            } else if (expenseMonth.equals(previousMonth)) {

                previousMonthTotal += expense.getAmount();
            }
        }final double totalForPercentage = currentMonthTotal;

        // Category-wise spending for the current month
        // Category-wise spending for the current month
        List<SpendSenseSummary.CategorySpending> categoryBreakdown =
                categoryTotals.entrySet()
                        .stream()
                        .map(entry -> new SpendSenseSummary.CategorySpending(
                                entry.getKey(),
                                entry.getValue(),
                                totalForPercentage > 0
                                        ? (entry.getValue() / totalForPercentage) * 100
                                        : 0
                        ))
                        .sorted((a, b) ->
                                Double.compare(b.amount(), a.amount()))
                        .toList();
        // Month-over-month percentage change
        Double percentageChange = previousMonthTotal > 0
                ? ((currentMonthTotal - previousMonthTotal)
                / previousMonthTotal) * 100
                : null;

        SpendSenseSummary.MonthlyComparison monthlyComparison =
                new SpendSenseSummary.MonthlyComparison(
                        currentMonthTotal,
                        previousMonthTotal,
                        percentageChange
                );

        // Rule-based personalized recommendations
        List<String> recommendations = new java.util.ArrayList<>();

        if (currentMonthTotal == 0) {

            recommendations.add(
                    "No expenses recorded this month. Add transactions to receive spending insights."
            );

        } else {

            if (!categoryBreakdown.isEmpty()) {
                SpendSenseSummary.CategorySpending highestCategory =
                        categoryBreakdown.get(0);

                if (highestCategory.percentage() >= 40) {
                    recommendations.add(
                            "You are spending "
                                    + String.format("%.1f", highestCategory.percentage())
                                    + "% of your monthly budget on "
                                    + highestCategory.category()
                                    + ". Consider reviewing this category."
                    );
                }
            }

            if (percentageChange != null && percentageChange >= 20) {
                recommendations.add(
                        "Your spending has increased by "
                                + String.format("%.1f", percentageChange)
                                + "% compared to last month. Review your recent expenses."
                );

            } else if (percentageChange != null && percentageChange <= -10) {
                recommendations.add(
                        "Your spending has decreased by "
                                + String.format("%.1f", Math.abs(percentageChange))
                                + "% compared to last month. Keep maintaining this pattern."
                );
            }

            if (recommendations.isEmpty()) {
                recommendations.add(
                        "Your spending looks relatively balanced. Keep tracking your expenses to maintain this pattern."
                );
            }
        }

        return new SpendSenseSummary(
                currentMonthTotal,
                categoryBreakdown,
                monthlyComparison,
                recommendations
        );
    }
}