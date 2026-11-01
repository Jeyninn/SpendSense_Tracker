package com.expensetracker.dto;

import java.time.LocalDate;

public record RecentTransactionResponse(
        Long id,
        String title,
        Double amount,
        String category,
        LocalDate date,
        String type
) {}