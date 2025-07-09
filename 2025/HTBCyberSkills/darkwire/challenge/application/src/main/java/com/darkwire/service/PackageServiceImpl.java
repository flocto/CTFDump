package com.darkwire.service;

import com.darkwire.model.Package;
import com.darkwire.model.User;
import com.darkwire.repository.PackageRepository;
import com.darkwire.util.ZipUtils;
import com.darkwire.util.PackageValidator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.List;
import java.util.zip.ZipInputStream;
import java.io.File;

@Service
public class PackageServiceImpl implements PackageService {

    @Autowired private PackageRepository packageRepository;

    private static final String PACKAGE_DIR = "src/main/resources/packages/";

    @Override
    public void savePackage(String name, String version, String type, String description, MultipartFile file, User uploader) {
        try {
            if (!file.getOriginalFilename().endsWith(".zip")) {
                throw new IllegalArgumentException("Only ZIP files are allowed.");
            }

            try (ZipInputStream zis = new ZipInputStream(file.getInputStream())) {
                boolean valid = PackageValidator.validateStructure(zis, name);
                if (!valid) {
                    throw new IllegalArgumentException("Invalid ZIP structure. Required: " + name + "/MANIFEST.xml, README.md, and RESOURCES/");
                }
            }

            String filename = System.currentTimeMillis() + "_" + file.getOriginalFilename();
            Path tempZipPath = Paths.get(PACKAGE_DIR + filename);
            Files.write(tempZipPath, file.getBytes());
        
            ZipUtils.unzip(tempZipPath.toFile(), new File(PACKAGE_DIR));
        
            Package pkg = new Package();
            pkg.setName(name);
            pkg.setVersion(version);
            pkg.setType(type);
            pkg.setDescription(description);
            pkg.setFilename(filename);
            pkg.setStatus("ACTIVE");
            pkg.setUploadedAt(LocalDateTime.now());
            pkg.setUploadedBy(uploader);
        
            packageRepository.save(pkg);
        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("IO Error: " + e.getMessage());
        }
    }

    @Override
    public void toggleStatus(Long id) {
        com.darkwire.model.Package pkg = packageRepository.findById(id).orElseThrow();
        String current = pkg.getStatus();
        pkg.setStatus("ACTIVE".equals(current) ? "INACTIVE" : "ACTIVE");
        packageRepository.save(pkg);
    }

    @Override
    public List<Package> findAll() {
        return packageRepository.findAll();
    }

    @Override
    public void deletePackage(Long id) {
        com.darkwire.model.Package pkg = packageRepository.findById(id).orElseThrow();
        String filename = pkg.getFilename();
        File file = new File(PACKAGE_DIR + filename);
        if (file.exists()) {
            file.delete();
        }
        packageRepository.delete(pkg);
    }
}
