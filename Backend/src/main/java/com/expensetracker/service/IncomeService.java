
package com.expensetracker.service;

import com.expensetracker.entity.Income;
import com.expensetracker.entity.User;
import com.expensetracker.exception.ResourceNotFoundException;
import com.expensetracker.repository.IncomeRepository;
import com.expensetracker.repository.UserRepository;

import org.springframework.stereotype.Service;
import org.springframework.security.core.context.SecurityContextHolder;

import java.util.List;

@Service
public class IncomeService {

    private final IncomeRepository incomeRepository;
    private final UserRepository userRepository;

    public IncomeService(
            IncomeRepository incomeRepository,
            UserRepository userRepository) {
        this.incomeRepository = incomeRepository;
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

    public List<Income> getAllIncomes() {
        User user = getCurrentUser();

        return incomeRepository.findAllByUser_Id(user.getId());
    }

    public Income addIncome(Income income) {
        User user = getCurrentUser();

        income.setUser(user);

        return incomeRepository.save(income);
    }

    public void deleteIncome(Long id) {
        User user = getCurrentUser();

        Income income = incomeRepository
                .findByIdAndUser_Id(id, user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Income not found"));

        incomeRepository.delete(income);
    }

    public Income updateIncome(Long id, Income updatedIncome) {
        User user = getCurrentUser();

        Income existingIncome = incomeRepository
                .findByIdAndUser_Id(id, user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Income not found"));

        existingIncome.setSource(updatedIncome.getSource());
        existingIncome.setAmount(updatedIncome.getAmount());
        existingIncome.setCategory(updatedIncome.getCategory());
        existingIncome.setDate(updatedIncome.getDate());
        existingIncome.setDescription(updatedIncome.getDescription());

        return incomeRepository.save(existingIncome);
    }
}
