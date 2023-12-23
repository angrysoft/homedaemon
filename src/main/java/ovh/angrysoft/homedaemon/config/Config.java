package ovh.angrysoft.homedaemon.config;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

public class Config {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");

    private String configBaseDir;
    private Map<String, ConfigType<?>> configs;

    public Config(String configBaseDir) {
        this.configBaseDir = configBaseDir;
        this.configs = new HashMap<>();
    }

    public <T> void resisterConfigType(String name, ConfigType<T> configType) {
        StringBuilder filePath = new StringBuilder(configBaseDir);
        filePath.append("/")
                .append(name)
                .append(".json");
        configType.setFilePath(filePath.toString());
        try {
            configType.setConfigData(
                    new Gson().fromJson(new FileReader(filePath.toString()), configType.getConfigClass()));
        } catch (FileNotFoundException e) {
            LOGGER.log(Level.ALL, "Config file {0} not found", configType.getFilePath());
        } catch (JsonSyntaxException e) {
            LOGGER.log(Level.ALL, "Config file parse error", configType.getFilePath());
        }
        this.configs.put(name, configType);
    }

    // public void loadConfig(String name) {
    //     if (configs.containsKey(name)) {
    //         ConfigType configT = configsTypes.get(name);
    //         try {
    //             configsData.put(name, new Gson().fromJson(new FileReader(configT.filePath()), configT.configType()));
    //         } catch (FileNotFoundException e) {
    //             LOGGER.log(Level.ALL, "Config file {0} not found", configT.filePath());
    //         } catch (JsonSyntaxException e) {
    //             LOGGER.log(Level.ALL, "Config file parse error", configT.filePath());
    //         }
    //     }
    // }

    // TODO what object should i return (Optional) when config is not loaded
    // (FileNotFount etc)
    public Record get(String configName) {
        ConfigType<?> conf = configs.get(configName);
        return (Record) conf.getConfigData();
    }
}
