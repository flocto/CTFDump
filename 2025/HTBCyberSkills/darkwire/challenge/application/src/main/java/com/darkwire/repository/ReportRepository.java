package com.darkwire.repository;

import com.darkwire.model.Report;
import com.darkwire.model.ReportStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReportRepository extends JpaRepository<Report, Long> {
    List<Report> findByUserId(Long userId);
    List<Report> findByStatus(ReportStatus status);
}
