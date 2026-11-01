package com.expensetracker.dto;

import java.time.LocalDate;

public record ExpenseResponse(
        Long id,
        String title,
        Double amount,
        String category,
        LocalDate date,
        String description
) {}