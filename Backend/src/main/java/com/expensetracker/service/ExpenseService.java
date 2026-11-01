
package com.expensetracker.service;

import com.expensetracker.dto.ExpenseRequest;
import com.expensetracker.dto.ExpenseResponse;
import com.expensetracker.entity.User;
import com.expensetracker.exception.ResourceNotFoundException;
import com.expensetracker.repository.ExpenseRepository;
import com.expensetracker.repository.UserRepository;
import com.expensetracker.entity.Expense;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ExpenseService {

    private final ExpenseRepository expenseRepository;
    private final UserRepository userRepository;

    public ExpenseService(
            ExpenseRepository expenseRepository,
            UserRepository userRepository) {
        this.expenseRepository = expenseRepository;
        this.userRepository = userRepository;
    }

    private User getCurrentUser() {
        String email = SecurityContextHolder
                .getContext()
                .getAuthentication()
                .getName();

        return userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));
    }

    private ExpenseResponse toResponse(Expense expense) {
        return new ExpenseResponse(
                expense.getId(),
                expense.getTitle(),
                expense.getAmount(),
                expense.getCategory(),
                expense.getDate(),
                expense.getDescription()
        );
    }

    public List<ExpenseResponse> getAllExpenseResponses() {
        User user = getCurrentUser();

        return expenseRepository.findAllByUser_Id(user.getId())
                .stream()
                .map(this::toResponse)
                .toList();
    }

    public ExpenseResponse addExpense(ExpenseRequest request) {
        User user = getCurrentUser();

        Expense expense =
                new Expense();

        expense.setTitle(request.title());
        expense.setAmount(request.amount());
        expense.setCategory(request.category());
        expense.setDate(request.date());
        expense.setDescription(request.description());
        expense.setUser(user);

        return toResponse(expenseRepository.save(expense));
    }

    public ExpenseResponse updateExpense(
            Long id,
            ExpenseRequest request) {

        User user = getCurrentUser();

       Expense existingExpense =
                expenseRepository.findByIdAndUser_Id(id, user.getId())
                        .orElseThrow(() ->
                                new ResourceNotFoundException("Expense not found"));

        existingExpense.setTitle(request.title());
        existingExpense.setAmount(request.amount());
        existingExpense.setCategory(request.category());
        existingExpense.setDate(request.date());
        existingExpense.setDescription(request.description());

        return toResponse(expenseRepository.save(existingExpense));
    }

    public Page<ExpenseResponse> getExpensesPaginated(int page, int size) {
        User user = getCurrentUser();

        Pageable pageable = PageRequest.of(
                page,
                size,
                Sort.by("date").descending()
        );

        return expenseRepository
                .findAllByUser_Id(user.getId(), pageable)
                .map(this::toResponse);
    }

    public void deleteExpense(Long id) {
        User user = getCurrentUser();

        Expense expense =
                expenseRepository.findByIdAndUser_Id(id, user.getId())
                        .orElseThrow(() ->
                                new ResourceNotFoundException("Expense not found"));

        expenseRepository.delete(expense);
    }
}
