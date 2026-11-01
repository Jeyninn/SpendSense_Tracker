
package com.expensetracker.repository;

import com.expensetracker.entity.Expense;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
public interface ExpenseRepository extends JpaRepository<Expense, Long> {
    Page<Expense> findAllByUser_Id(Long userId, Pageable pageable);
    List<Expense> findAllByUser_Id(Long userId);
    List<Expense> findAllByUser_IdOrderByDateAscIdAsc(Long userId);
    Optional<Expense> findByIdAndUser_Id(Long id, Long userId);
    List<Expense> findTop5ByUser_IdOrderByDateDescIdDesc(Long userId);

    long countByUser_Id(Long userId);
    @Query("""
    SELECT COALESCE(SUM(e.amount), 0.0)
    FROM Expense e
    WHERE e.user.id = :userId
""")
    Double getTotalExpenseByUserId(@Param("userId") Long userId);

    @Query("""
    SELECT e.category, SUM(e.amount)
    FROM Expense e
    WHERE e.user.id = :userId
    GROUP BY e.category
""")
    List<Object[]> getCategoryTotalsByUserId(@Param("userId") Long userId);
}
