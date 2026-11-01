
package com.expensetracker.service;

import com.expensetracker.dto.SignupRequest;
import com.expensetracker.dto.LoginRequest;
import com.expensetracker.dto.AuthResponse;

import com.expensetracker.entity.User;
import com.expensetracker.repository.UserRepository;
import com.expensetracker.security.JwtService;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;

    public AuthService(
            UserRepository userRepository,
            PasswordEncoder passwordEncoder,
            AuthenticationManager authenticationManager,
            JwtService jwtService) {

        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtService = jwtService;
    }

    // SIGNUP
    public AuthResponse register(SignupRequest request) {

        // Check if email already exists
        if (userRepository.existsByEmail(request.email())) {
            throw new RuntimeException("Email already registered");
        }

        // Create new user
        User user = new User();

        user.setName(request.name());
        user.setEmail(request.email());

        // Encrypt password
        user.setPassword(passwordEncoder.encode(request.password()));

        // Save user in database
        userRepository.save(user);

        // Generate JWT
        String token = jwtService.generateToken(user.getEmail());

        return new AuthResponse(
                token,
                user.getName(),
                user.getEmail()
        );
    }

    // LOGIN
    public AuthResponse login(LoginRequest request) {

        // Authenticate user credentials
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.email(),
                        request.password()
                )
        );

        // Fetch user
        User user = userRepository.findByEmail(request.email())
                .orElseThrow(() ->
                        new RuntimeException("User not found"));

        // Generate JWT
        String token = jwtService.generateToken(user.getEmail());

        return new AuthResponse(
                token,
                user.getName(),
                user.getEmail()
        );
    }
}
