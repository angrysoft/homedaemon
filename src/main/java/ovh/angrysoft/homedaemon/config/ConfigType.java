package ovh.angrysoft.homedaemon.config;

public class ConfigType<T> {
    protected String filePath;
    protected Class<T> configClass;
    protected T configData;

    public ConfigType(Class<T> configClass) {
        this.filePath = "";
        this.configClass = configClass;
    }

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public Class<T> getConfigClass() {
        return configClass;
    }

    public void setConfigData(T configData) {
        this.configData = configData;
    }

    public T getConfigData() {
        return configData;
    }
}
