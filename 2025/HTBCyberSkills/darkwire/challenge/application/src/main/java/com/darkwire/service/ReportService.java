package com.darkwire.service;

import com.darkwire.model.Report;
import com.darkwire.model.ReportStatus;
import com.darkwire.model.User;
import com.darkwire.repository.ReportRepository;
import com.darkwire.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class ReportService {

    private static final String UPLOAD_DIR = "src/main/resources/static/uploads";

    @Autowired
    private ReportRepository reportRepository;

    @Autowired
    private UserRepository userRepository;

    public Report saveReport(String username, String title, String description, String department, MultipartFile file) throws IOException {
        // Filter for .pdf, .docx files only. Only pdf or docx files are allowed.
        if (!file.getOriginalFilename().endsWith(".pdf") && !file.getOriginalFilename().endsWith(".docx")) {
            throw new IllegalArgumentException("Only .pdf and .docx files are allowed.");
        }

        Files.createDirectories(Paths.get(UPLOAD_DIR));

        String fileName = System.currentTimeMillis() + "_" + file.getOriginalFilename();
        Path filePath = Paths.get(UPLOAD_DIR, fileName);
        Files.write(filePath, file.getBytes());

        User user = userRepository.findByUsername(username).orElseThrow();

        Report report = new Report();
        report.setUser(user);
        report.setTitle(title);
        report.setDescription(description);
        report.setFileName(fileName);
        report.setUploadedAt(LocalDateTime.now());
        report.setStatus(ReportStatus.PENDING);
        report.setDepartment(department);
        return reportRepository.save(report);
    }

    public List<Report> findEmployeeAll(String username) {
        // find reports by user id
        User user = userRepository.findByUsername(username).orElseThrow();
        return reportRepository.findByUserId(user.getId());
    }

    public List<Report> findAll() {
        return reportRepository.findAll();
    }

    public Optional<Report> findById(Long id) {
        return reportRepository.findById(id);
    }

    public void updateStatus(Long id, ReportStatus status) {
        Optional<Report> opt = reportRepository.findById(id);
        opt.ifPresent(report -> {
            report.setStatus(status);
            reportRepository.save(report);
        });
    }

    public byte[] getFileContent(String fileName) throws IOException {
        Path path = Paths.get(UPLOAD_DIR).resolve(fileName);
        return Files.readAllBytes(path);
    }

    public long reportIDgen(){
        // random number between 2^10 and 2^20
        int min = (int) Math.pow(2, 10);
        int max = (int) Math.pow(2, 20);
        return (long) (Math.random() * (max - min + 1) + min);
    }
}