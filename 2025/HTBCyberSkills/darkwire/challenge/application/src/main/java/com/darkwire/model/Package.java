package com.darkwire.model;

import jakarta.persistence.*; 
import java.time.LocalDateTime;

@Entity public class Package {

@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;

private String name;
private String version;
private String type;

@Column(columnDefinition = "TEXT")
private String description;

private String filename;
private String status;

private LocalDateTime uploadedAt;

@ManyToOne
@JoinColumn(name = "uploaded_by")
private User uploadedBy;

// Getters and Setters

public Long getId() { return id; }

public void setId(Long id) { this.id = id; }

public String getName() { return name; }

public void setName(String name) { this.name = name; }

public String getVersion() { return version; }

public void setVersion(String version) { this.version = version; }

public String getType() { return type; }

public void setType(String type) { this.type = type; }

public String getDescription() { return description; }

public void setDescription(String description) { this.description = description; }

public String getFilename() { return filename; }

public void setFilename(String filename) { this.filename = filename; }

public String getStatus() { return status; }

public void setStatus(String status) { this.status = status; }

public LocalDateTime getUploadedAt() { return uploadedAt; }

public void setUploadedAt(LocalDateTime uploadedAt) { this.uploadedAt = uploadedAt; }

public User getUploadedBy() { return uploadedBy; }

public void setUploadedBy(User uploadedBy) { this.uploadedBy = uploadedBy; }

}