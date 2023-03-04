package ovh.angrysoft.homedaemon.config;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.stream.Stream;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

public class Config {
    private HashMap<String, HashMap<String, ConfigValue<T>>> data;
    private static final Logger LOGGER = Logger.getLogger(Config.class.getName());

    public Config() {
        data = new HashMap<>();
    }

    public HashMap<String, ConfigValue<?>> getCategory(String name) {
        if (data.containsKey(name)) {
            return (HashMap<String, ConfigValue<?>>) data.get(name);
        }
        return null;
    }

    public <T> T get(String category, String key) {
        if (data.containsKey(category)) {
            HashMap<String, ConfigValue<?>> cat = data.get(category);
            return (T) cat.get(key);
        }
        return null;
    }

    public <T> void set(String categoryName, HashMap<String, ConfigValue<T>> category) {
        data.put(categoryName, category);
    }

    public void loadFromDir(String dirPath) throws IOException {
        Path path = Paths.get(dirPath);
        try (Stream<Path> paths = Files.walk(path, 1)) {
            for (Path file : paths.filter(Files::isRegularFile)
                    .filter(f -> f.getFileName().toString().endsWith(".json"))
                    .toList()) {

                loadConfigFile(file);
            }
        }
    }

    public void listCategory() {
        data.forEach((cat, val) -> {
            System.err.println(cat);
        });
    }

    /**
     * @param path
     * @throws FileNotFoundException
     */
    private <T> void loadConfigFile(Path path) {
        try {
            Gson gson = new Gson();
            HashMap<String, ConfigValue<T>> conf = new HashMap<>();
            conf = (HashMap<String, ConfigValue<T>>) gson.fromJson(new FileReader(path.toString()), HashMap.class);
            String fileName = path.getFileName().toString();
            String[] name = fileName.split(".json");
            set(name[0], conf);
        } catch (FileNotFoundException e) {
            LOGGER.log(Level.ALL, "Config file {0} not found", path.getFileName().toString());
        } catch (JsonSyntaxException e) {
            LOGGER.log(Level.ALL, "Config file parse error", path.getFileName().toString());
        }

    }
}
