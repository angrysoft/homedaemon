package ovh.angrysoft.homedaemon.config;

class ConfigValue<T> {
    private T value;

    public void setValue( T newValue) {
        value = newValue;
    }
    
    public T get() {
        return value;
    }
}
