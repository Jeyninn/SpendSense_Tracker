package com.expensetracker.controller;

import com.expensetracker.dto.SpendSenseInsight;
import com.expensetracker.entity.User;
import com.expensetracker.exception.ResourceNotFoundException;
import com.expensetracker.repository.UserRepository;
import com.expensetracker.service.SpendSenseService;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import com.expensetracker.dto.SpendSenseSummary;
import java.util.List;

@RestController
@RequestMapping("/api/spendsense")
public class SpendSenseController {

    private final SpendSenseService spendSenseService;
    private final UserRepository userRepository;

    public SpendSenseController(
            SpendSenseService spendSenseService,
            UserRepository userRepository
    ) {
        this.spendSenseService = spendSenseService;
        this.userRepository = userRepository;
    }

    @GetMapping("/insights")
    public ResponseEntity<List<SpendSenseInsight>> getInsights(
            Authentication authentication
    ) {

        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found"));

        List<SpendSenseInsight> insights =
                spendSenseService.analyzeExpenses(user.getId());

        return ResponseEntity.ok(insights);
    }


    @GetMapping("/summary")
    public ResponseEntity<SpendSenseSummary> getSpendingSummary(
            Authentication authentication
    ) {

        // Get logged-in user's email
        String email = authentication.getName();

        // Find the user
        User user = userRepository.findByEmail(email)
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found"));

        // Generate spending summary
        SpendSenseSummary summary =
                spendSenseService.getSpendingSummary(user.getId());

        return ResponseEntity.ok(summary);
    }
}