package ovh.angrysoft.homedaemon.config;

import java.util.HashMap;
import java.util.Map;

import com.google.gson.Gson;

public class Config {
    private String configBaseDir;
    private Map<String, Record> configsData;
    private Map<String, Class<Record>> configsTypes;

    public Config(String configBaseDir) {
        this.configBaseDir = configBaseDir;
        this.configsData = new HashMap<>();
        this.configsTypes = new HashMap<>();
    }

    public void resisterConfigType(String name, Class<Record> configType) {
        StringBuilder filePath = new StringBuilder(configBaseDir);
        filePath.append("/")
                .append(name)
                .append(".json");
        this.configsTypes.put(name, new ConfigType());
    }

    public void loadConfig(String name) {
        if (configsTypes.containsKey(name)) {
            try {
                Record conf = new Gson().fromJson(new FileReader(config), JsonObject.class);
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
}

class ConfigType {
    private String filePath;
    private Calss<Record> configType;

    public ConfigType(file) {

    }
}
