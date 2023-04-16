package ovh.angrysoft.homedaemon.config;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.stream.Stream;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSyntaxException;

public class Config {
    private HashMap<String, JsonObject> data;
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");

    public Config() {
        data = new HashMap<>();
    }

    private JsonObject getCategory(String name) {
        if (data.containsKey(name)) {

            return data.get(name);
        }
        return null;
    }

    public JsonElement get(String category, String key) {
        JsonObject cat = getCategory(category);
        if (cat != null) {
            return cat.get(key);
        }
        return null;
    }

    public boolean hasKeyInCategory(String category, String key) {
        JsonObject cat = getCategory(category);
        if (cat != null)
            return cat.has(key);

        return false;
    }

    public void setCategory(String categoryName, JsonObject category) {
        data.put(categoryName, category);
    }

    public void loadConfigs(String dirPath) {
        Path path = Paths.get(dirPath);
        if (!Files.isDirectory(path))
            LOGGER.log(Level.ALL, "Reading dir error {0}", path.getFileName());

        try (Stream<Path> paths = Files.walk(path, 1)) {
            for (Path file : paths.filter(Files::isRegularFile)
                    .filter(f -> f.getFileName().toString().endsWith(".json"))
                    .toList()) {

                loadConfigFile(file);
            }
        } catch (IOException e) {
            LOGGER.log(Level.ALL, "Reading dir error {0}", e.getMessage());
        }
    }

    public Set<String> categorySet() {
        return data.keySet();
    }

    /**
     * @param path - directory witch json configs
     * @throws FileNotFoundException
     */
    private void loadConfigFile(Path path) {
        try {
            JsonObject conf = new Gson().fromJson(new FileReader(path.toString()), JsonObject.class);
            String fileName = path.getFileName().toString();
            String[] name = fileName.split(".json");
            setCategory(name[0], conf);
        } catch (FileNotFoundException e) {
            LOGGER.log(Level.ALL, "Config file {0} not found", path.getFileName().toString());
        } catch (JsonSyntaxException e) {
            LOGGER.log(Level.ALL, "Config file parse error", path.getFileName().toString());
        }

    }
}
