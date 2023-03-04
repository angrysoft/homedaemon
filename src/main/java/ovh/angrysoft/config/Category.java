package ovh.angrysoft.config;

import java.util.HashMap;

class Category {
    private HashMap<String, Object> category = new HashMap<>();

    public <T> T get(String key) {
        if (category.containsKey(key)) {
            return (T) category.get(key);
        }
        return null;
    }

    public <T> void set(String key, T valueT) {
        category.put(key, valueT);
    }
}
