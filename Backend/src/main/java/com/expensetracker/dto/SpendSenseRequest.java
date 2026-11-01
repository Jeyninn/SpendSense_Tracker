package com.expensetracker.dto;

public record SpendSenseRequest(
        Double amount,
        String category,
        Integer hour,

        @com.fasterxml.jackson.annotation.JsonProperty("day_of_week")
        Integer dayOfWeek,

        @com.fasterxml.jackson.annotation.JsonProperty("reference_amount")
        Double referenceAmount,

        @com.fasterxml.jackson.annotation.JsonProperty("has_personal_history")
        Boolean hasPersonalHistory
) {
}