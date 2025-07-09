package com.darkwire.service;

import com.darkwire.model.Package;
import com.darkwire.model.User;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

public interface PackageService {
    void savePackage(String name, String version, String type, String description, MultipartFile file, User uploader) throws IOException;
    void toggleStatus(Long id);
    void deletePackage(Long id);
    List<Package> findAll();
}
