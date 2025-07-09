package com.darkwire.util;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ZipUtils {

    public static void unzip(File zipFile, File outputDir) throws IOException {
        String outputPath = RandomPrefix();

        try (ZipInputStream zis = new ZipInputStream(new FileInputStream(zipFile))) {
            ZipEntry entry;

            while ((entry = zis.getNextEntry()) != null) {
                File outFile = new File(outputDir, outputPath + "/" + entry.getName());
                
                if (entry.isDirectory()) {
                    outFile.mkdirs();
                } else {
                    outFile.getParentFile().mkdirs();
                    try (FileOutputStream fos = new FileOutputStream(outFile)) {
                        byte[] buffer = new byte[1024];
                        int len;
                        while ((len = zis.read(buffer)) > 0) {
                            fos.write(buffer, 0, len);
                        }
                    }
                }
            }
        }
    }


    public static String RandomPrefix() {
        StringBuilder prefix = new StringBuilder();
        for (int i = 0; i < 10; i++) {
            int randomChar = (int) (Math.random() * 26) + 'a';
            prefix.append((char) randomChar);
        }
        return prefix.toString();
    }
}
