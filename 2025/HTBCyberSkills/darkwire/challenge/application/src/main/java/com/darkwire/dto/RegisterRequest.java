package com.darkwire.dto;

public class RegisterRequest {

    private String username;
    private String password;
    private String email;
    private String fullName;
    private String department;

    public RegisterRequest() {
    }

    public RegisterRequest(String username, String password, String email, String fullName, String department) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.fullName = fullName;
        this.department = department;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getEmail() {
        return email;
    }

    public String getFullName() {
        return fullName;
    }

    public String getDepartment() {
        return department;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public void setDepartment(String department) {
        this.department = department;
    }
}
