package com.darkwire.controller;

import com.darkwire.dto.RegisterRequest;
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
public class AuthController {

    private final UserRepository userRepo;
    private final org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder encoder;

    public AuthController(UserRepository userRepo,
                          org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder encoder) {
        this.userRepo = userRepo;
        this.encoder = encoder;
    }

    @GetMapping("/login")
    public String loginPage(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null && session.getAttribute("user") != null) {
            return "forward:/dashboard";  // direct forward
        }
        return "login";
    }

    @PostMapping("/login")
    public ResponseEntity<Void> login(@RequestParam String username,
                                      @RequestParam String password,
                                      HttpServletRequest request,
                                      RedirectAttributes redirectAttrs) {
        Optional<User> userOpt = userRepo.findByUsername(username);
        if (userOpt.isEmpty() || !encoder.matches(password, userOpt.get().getPassword())) {
            redirectAttrs.addFlashAttribute("error", "Invalid username or password");
            HttpHeaders headers = new HttpHeaders();
            headers.setLocation(URI.create("/login?error"));
            return new ResponseEntity<>(headers, HttpStatus.FOUND);
        }

        User user = userOpt.get();
        HttpSession session = request.getSession();
        session.setAttribute("user", user);
        session.setMaxInactiveInterval(30 * 60);

        String target = user.getRole() == Role.ROLE_MANAGER
                ? "/manager/dashboard"
                : "/employee/dashboard";
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create(target));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }

    @GetMapping("/logout")
    public ResponseEntity<Void> logout(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null) session.invalidate();
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create("/login"));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }

    @GetMapping("/register")
    public String registerPage(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null && session.getAttribute("user") != null) {
            return "forward:/dashboard";
        }
        return "register";
    }

    @PostMapping("/register")
    public ResponseEntity<Void> registerUser(@ModelAttribute RegisterRequest request,
                                             RedirectAttributes redirectAttrs) {
        if (userRepo.findByUsername(request.getUsername()).isPresent()) {
            redirectAttrs.addFlashAttribute("error", "Username already exists");
            HttpHeaders headers = new HttpHeaders();
            headers.setLocation(URI.create("/register"));
            return new ResponseEntity<>(headers, HttpStatus.FOUND);
        }
        User user = new User();
        user.setUsername(request.getUsername());
        user.setPassword(encoder.encode(request.getPassword()));
        user.setEmail(request.getEmail());
        user.setFullName(request.getFullName());
        user.setDepartment(request.getDepartment());
        user.setRole(Role.ROLE_EMPLOYEE);
        userRepo.save(user);

        redirectAttrs.addFlashAttribute("success", "Registration successful. You can now log in.");
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create("/login"));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }
}
