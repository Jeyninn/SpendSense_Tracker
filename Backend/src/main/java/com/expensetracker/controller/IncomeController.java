package com.expensetracker.controller;

import com.expensetracker.entity.Income;
import com.expensetracker.service.IncomeService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/incomes")
@CrossOrigin(origins = "http://localhost:4200")
public class IncomeController {
    private final IncomeService incomeService;
    public IncomeController(IncomeService incomeService){
        this.incomeService=incomeService;
    }
    @GetMapping
    public List<Income> getAllIncomes(){
        return incomeService.getAllIncomes();
    }
    @PostMapping
    public Income addIncome(@RequestBody Income income){
        return incomeService.addIncome(income);
    }
    @DeleteMapping("/{id}")
    public void deleteIncome(@PathVariable Long id){
        incomeService.deleteIncome(id);
    }
    @PutMapping("/{id}")
    public Income updateIncome(
            @PathVariable Long id,
            @RequestBody Income income) {

        return incomeService.updateIncome(id, income);
    }

}
