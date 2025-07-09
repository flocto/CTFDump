package com.darkwire.controller;

import com.darkwire.model.Report;
import com.darkwire.model.ReportStatus;
import com.darkwire.model.Role;
import com.darkwire.model.User;
import com.darkwire.service.ReportService;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.net.URI;
import java.util.Optional;

@Controller
public class ReportController {

    private final ReportService reportService;
    public ReportController(ReportService reportService) {
        this.reportService = reportService;
    }

    @GetMapping("/employee/reports")
    public String listReportsForEmployee(Model model, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_EMPLOYEE) {
            return "redirect:/login";
        }
        String username = ((User)session.getAttribute("user")).getUsername();
        model.addAttribute("reports", reportService.findEmployeeAll(username));
        return "employee/report-list";
    }

    @GetMapping("/employee/upload-report")
    public String showUploadForm(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_EMPLOYEE) {
            return "redirect:/login";
        }
        return "employee/upload-report";
    }

    @PostMapping("/employee/upload-report")
    public ResponseEntity<Void> uploadReport(HttpServletRequest request,
                                             @RequestParam String title,
                                             @RequestParam String description,
                                             @RequestParam String department,
                                             @RequestParam MultipartFile file) throws IOException {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_EMPLOYEE) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        reportService.saveReport(((User)session.getAttribute("user")).getUsername(), title, description, department, file);
        HttpHeaders h = new HttpHeaders();
        h.setLocation(URI.create("/employee/reports"));
        return new ResponseEntity<>(h, HttpStatus.FOUND);
    }

    @GetMapping("/reports/download/{id}")
    public void download(@PathVariable Long id, HttpServletResponse response, HttpServletRequest request) throws IOException {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null) {
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }
        Report report = reportService.findById(id).orElseThrow();
        User user = (User) session.getAttribute("user");
        if (!report.getUser().getUsername().equals(user.getUsername())
            && user.getRole()!=Role.ROLE_MANAGER) {
            response.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        response.setContentType("application/octet-stream");
        response.setHeader("Content-Disposition", "attachment; filename=\"" + report.getFileName() + "\"");
        response.getOutputStream().write(reportService.getFileContent(report.getFileName()));
        response.flushBuffer();
    }

    @GetMapping("/manager/reports")
    public String listReportsForManager(Model model, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_MANAGER) {
            return "redirect:/login";
        }
        model.addAttribute("reports", reportService.findAll());
        return "manager/report-list";
    }

    @GetMapping("/manager/reports/review/{id}")
    public String showReview(@PathVariable Long id, Model model, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_MANAGER) {
            return "redirect:/login";
        }
        Report report = reportService.findById(id).orElseThrow();
        model.addAttribute("report", report);
        return "manager/review-report";
    }

    @PostMapping("/manager/reports/review/{id}")
    public ResponseEntity<Void> handleReview(@PathVariable Long id,
                                             @RequestParam String action,
                                             HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_MANAGER) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        ReportStatus status = action.equals("approve") ? ReportStatus.APPROVED : ReportStatus.REJECTED;
        reportService.updateStatus(id, status);
        HttpHeaders h = new HttpHeaders();
        h.setLocation(URI.create("/manager/reports"));
        return new ResponseEntity<>(h, HttpStatus.FOUND);
    }
}
