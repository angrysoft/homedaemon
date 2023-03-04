package ovh.angrysoft.config;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.stream.Stream;

public class Config {
    private HashMap<String, Category> data;

    public Config() {
        data = new HashMap<>();
    }

    public void loadFromDir(String dir) throws IOException {
        try (Stream<Path> paths = Files.walk(Paths.get(dir))) {
            for (Path path: paths.filter(Files::isRegularFile).filter(f -> f.getFileName().endsWith(".json")).toList()) {
                System.err.println(path.getFileName());
            }
        }
    }
}
