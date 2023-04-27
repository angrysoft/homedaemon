package ovh.angrysoft.homedaemon.devices;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Logger;

import ovh.angrysoft.homedaemon.discover.DiscoverEngine;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeAlreadyExist;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;
import ovh.angrysoft.homedaemon.watcher.Watcher;

public abstract class BaseDevice {
    protected final DeviceStatus status;
    protected final Set<String> commands;
    protected boolean discoverable = false;
    protected DiscoverEngine discoverEngine = null;
    protected Watcher watcher = null;
    protected boolean gatewayNeeded = false;

    protected final Logger LOGGER = Logger.getLogger("Homedaemon");

    protected BaseDevice(DeviceInfo deviceInfo) {
        this.status = new DeviceStatus();
        this.commands = new HashSet<>();
        this.setupCommandSet();
        try {
            this.status.registerAttribute(new DeviceAttribute<String>("sid", deviceInfo.getSid(), true));
            this.status.registerAttribute(new DeviceAttribute<Map<String, String>>("name", deviceInfo.getName()));
            this.status.registerAttribute(new DeviceAttribute<Map<String, String>>("place", deviceInfo.getPlace()));
        } catch (AttributeAlreadyExist e) {
            LOGGER.warning(e.getMessage());
        }
    }

    // For thinks like setup watcher
    public abstract void setup();

    public Watcher getWatcher() {
        return watcher;
    }

    public boolean isDiscoverable() {
        return discoverable;
    }

    public DiscoverEngine getDiscoverEngine() {
        return discoverEngine;
    }

    public Set<String> getCommands() {
        return commands;
    }

    protected String getSid() {
        return this.status.get("sid");
    }

    protected void setupCommandSet() {
        getAllMethods(this.getClass());
    }

    private void getAllMethods(Class<?> cls) {
        if (!(cls.getSuperclass().getSimpleName().equals("Object"))) {
            getAllMethods(cls.getSuperclass());
        }

        for (Class<?> inter : cls.getInterfaces()) {
            for (Method method : inter.getDeclaredMethods()) {
                this.commands.add(method.getName());
            }
        }
    }

    public List<String> getTraits() {
        List<String> ret = new ArrayList<>();
        for (Class<?> cls : this.getClass().getInterfaces()) {
            String className = cls.getName();
            int lastDot = className.lastIndexOf(".");
            ret.add(className.substring(++lastDot));
        }
        return ret;
    }

    public <T> T query(String attrName) {
        return this.status.get(attrName);
    }

    public Map<String, String> getDeviceStatus() {
        HashMap<String, String> ret = new HashMap<>();
        ret.putAll(this.status.getAll());
        ret.put("traits", this.getTraits().toString());
        return ret;

    }

    public <T> Boolean updateStatus(String attrName, T attrValue) throws AttributeReadOnly {
        return this.status.update(attrName, attrValue);
    }

    /**
     * Execute allowed method from device commands
     * executed method arguments must by not a primitive type
     * 
     * @param methodName method to be executed
     * @param arg        arg optional method argument
     */
    public void execute(String methodName, Object arg) {
        if (!this.commands.contains(methodName)) {
            LOGGER.warning(String.format("Executing %s of %s is not allowed", methodName, this.getClass()));
            return;
        }

        try {
            if (arg != null) {
                Method cmd = this.getClass().getMethod(methodName, arg.getClass());
                cmd.invoke(this, arg);
                return;
            }
            Method cmd = this.getClass().getMethod(methodName);
            cmd.invoke(this);
        } catch (NoSuchMethodException | SecurityException e) {
            LOGGER.warning(e.getMessage());
            e.printStackTrace();
        } catch (InvocationTargetException | IllegalAccessException | IllegalArgumentException e) {
            LOGGER.warning(e.getMessage());
            e.printStackTrace();
        }
    }

    public boolean isGatewayNeeded() {
        return gatewayNeeded;
    }

    public void setGateway(Gateway gateway) {
        throw new UnsupportedOperationException("Unimplemented method 'setGateway'");
    }

}
