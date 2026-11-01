
package com.expensetracker.repository;

import com.expensetracker.entity.Income;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
public interface IncomeRepository extends JpaRepository<Income, Long> {
    List<Income> findTop5ByUser_IdOrderByDateDescIdDesc(Long userId);

    long countByUser_Id(Long userId);
    List<Income> findAllByUser_Id(Long userId);
    @Query("""
    SELECT COALESCE(SUM(i.amount), 0.0)
    FROM Income i
    WHERE i.user.id = :userId
""")
    Double getTotalIncomeByUserId(@Param("userId") Long userId);
    Optional<Income> findByIdAndUser_Id(Long id, Long userId);
}
