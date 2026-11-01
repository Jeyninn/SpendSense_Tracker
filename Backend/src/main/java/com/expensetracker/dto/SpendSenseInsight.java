package com.expensetracker.dto;

import java.time.LocalDate;

public record SpendSenseInsight(
        Long expenseId,
        String title,
        Double amount,
        String category,
        LocalDate date,
        SpendSenseResponse prediction
) {
}