package com.darkwire.controller;

import com.darkwire.model.Role;
import com.darkwire.model.User;
import com.darkwire.service.PackageService;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.net.URI;

@Controller
@RequestMapping("/manager/packages")
public class PackageController {

    private final PackageService packageService;
    public PackageController(PackageService packageService) {
        this.packageService = packageService;
    }

    @GetMapping
    public String list(Model model, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null
            || ((User)session.getAttribute("user")).getRole() != Role.ROLE_MANAGER) {
            return "redirect:/login";
        }
        model.addAttribute("packages", packageService.findAll());
        return "manager/package-list";
    }

    @GetMapping("/upload")
    public String uploadForm(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null
            || ((User)session.getAttribute("user")).getRole() != Role.ROLE_MANAGER) {
            return "redirect:/login";
        }
        return "manager/upload-package";
    }

    @PostMapping("/upload")
    public ResponseEntity<Void> upload(HttpServletRequest request,
                                       @RequestParam String name,
                                       @RequestParam String version,
                                       @RequestParam String type,
                                       @RequestParam String description,
                                       @RequestParam MultipartFile file) throws IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null
            || ((User)session.getAttribute("user")).getRole() != Role.ROLE_MANAGER) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        packageService.savePackage(name, version, type, description, file, (User)session.getAttribute("user"));
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create("/manager/packages"));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }

    @PostMapping("/toggle-status/{id}")
    public ResponseEntity<Void> togglePackageStatus(@PathVariable Long id, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_MANAGER) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        packageService.toggleStatus(id);
        HttpHeaders h = new HttpHeaders();
        h.setLocation(URI.create("/manager/packages"));
        return new ResponseEntity<>(h, HttpStatus.FOUND);
    }

    @PostMapping("/delete/{id}")
    public ResponseEntity<Void> deletePackage(@PathVariable Long id, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session==null || session.getAttribute("user")==null
            || ((User)session.getAttribute("user")).getRole()!=Role.ROLE_MANAGER) {
            HttpHeaders h = new HttpHeaders();
            h.setLocation(URI.create("/login"));
            return new ResponseEntity<>(h, HttpStatus.FOUND);
        }
        packageService.deletePackage(id);
        HttpHeaders h = new HttpHeaders();
        h.setLocation(URI.create("/manager/packages"));
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
