package com.darkwire.controller;

import com.darkwire.model.Role;
import com.darkwire.model.User;
import com.darkwire.repository.UserRepository;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import java.net.URI;
import java.util.Optional;

@Controller
public class DashboardController {

    private final UserRepository userRepository;
    private final org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder passwordEncoder;

    public DashboardController(UserRepository userRepository,
                               org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @GetMapping("/dashboard")
    public ResponseEntity<Void> redirectDashboard(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        User user = (User) session.getAttribute("user");
        String target = user.getRole() == Role.ROLE_MANAGER
                ? "/manager/dashboard"
                : "/employee/dashboard";
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create(target));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }

    @GetMapping("/manager/dashboard")
    public String managerDashboard(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null
            || ((User)session.getAttribute("user")).getRole() != Role.ROLE_MANAGER) {
            return "redirect:/login"; // you may leave single-case
        }
        return "manager/manager-dashboard";
    }

    @GetMapping("/employee/dashboard")
    public String employeeDashboard(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null
            || ((User)session.getAttribute("user")).getRole() != Role.ROLE_EMPLOYEE) {
            return "redirect:/login";
        }
        return "employee/employee-dashboard";
    }

    @GetMapping("/settings")
    public String settings(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            return "redirect:/login";
        }
        return "settings";
    }

    @PostMapping("/settings")
    public ResponseEntity<Void> updatePassword(HttpServletRequest request,
                                               @RequestParam String currentPassword,
                                               @RequestParam String newPassword,
                                               @RequestParam String confirmPassword,
                                               RedirectAttributes redirectAttributes) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        if (!newPassword.equals(confirmPassword)) {
            redirectAttributes.addFlashAttribute("error", "New password and confirmation do not match.");
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/settings"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        User user = (User) session.getAttribute("user");
        if (!passwordEncoder.matches(currentPassword, user.getPassword())) {
            redirectAttributes.addFlashAttribute("error", "Current password is incorrect.");
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/settings"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        user.setPassword(passwordEncoder.encode(newPassword));
        userRepository.save(user);
        redirectAttributes.addFlashAttribute("success", "Password updated successfully.");
        HttpHeaders h = new HttpHeaders();
        h.setLocation(URI.create("/settings"));
        return new ResponseEntity<>(h, HttpStatus.FOUND);
    }
    
    // Helper methods for authentication
    private boolean isAuthenticated(HttpServletRequest request) {
        return getCurrentUser(request) != null;
    }
    
    private User getCurrentUser(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            return (User) session.getAttribute("user");
        }
        return null;
    }
    
    private boolean hasRole(HttpServletRequest request, Role role) {
        User user = getCurrentUser(request);
        return user != null && user.getRole() == role;
    }
}
