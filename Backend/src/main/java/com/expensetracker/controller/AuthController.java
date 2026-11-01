
package com.expensetracker.controller;

import com.expensetracker.dto.SignupRequest;
import com.expensetracker.dto.LoginRequest;
import com.expensetracker.dto.AuthResponse;
import com.expensetracker.service.AuthService;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "http://localhost:4200")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    // Signup
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(
            @RequestBody SignupRequest request) {

        AuthResponse response = authService.register(request);

        return ResponseEntity.ok(response);
    }

    // Login
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(
            @RequestBody LoginRequest request) {
        AuthResponse response = authService.login(request);

        return ResponseEntity.ok(response);
    }
}
