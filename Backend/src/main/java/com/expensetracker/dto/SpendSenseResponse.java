package com.expensetracker.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record SpendSenseResponse(

        @JsonProperty("is_anomaly")
        Boolean isAnomaly,

        @JsonProperty("anomaly_score")
        Double anomalyScore,

        String severity,

        String explanation,

        @JsonProperty("model_version")
        String modelVersion

) {
}