package com.darkwire.util;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class PackageValidator {

    public static boolean validateStructure(ZipInputStream zipStream, String expectedRoot) throws IOException {
        Set<String> requiredEntries = new HashSet<>();
        requiredEntries.add(expectedRoot + "/MANIFEST.xml");
        requiredEntries.add(expectedRoot + "/README.md");
        requiredEntries.add(expectedRoot + "/RESOURCES/");

        Set<String> foundEntries = new HashSet<>();

        ZipEntry entry;
        while ((entry = zipStream.getNextEntry()) != null) {
            String name = entry.getName();

            if (entry.isDirectory() && !name.endsWith("/")) {
                name += "/";
            }

            for (String required : requiredEntries) {
                if (name.equals(required) || name.startsWith(required)) {
                    foundEntries.add(required);
                }
            }
        }

        return foundEntries.containsAll(requiredEntries);
    }
}
