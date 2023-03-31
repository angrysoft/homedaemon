package ovh.angrysoft.homedaemon.devices;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

import ovh.angrysoft.homedaemon.bus.EventBus;
import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;
import ovh.angrysoft.homedaemon.exceptions.attributes.AttributeReadOnly;
import ovh.angrysoft.homedaemon.exceptions.devices.DeviceNotSupported;
import ovh.angrysoft.homedaemon.exceptions.devices.GatewayNotFound;
import ovh.angrysoft.homedaemon.exceptions.discover.DeviceNotDiscovered;
import ovh.angrysoft.homedaemon.watcher.WatcherManager;

public class DeviceManager {
    private static final Logger LOGGER = Logger.getLogger("Homedaemon");
    private DeviceFactory deviceFactory;
    private String deviceInfoDir;
    private ArrayList<DeviceInfo> gatewaysInfoList;
    private ArrayList<DeviceInfo> devicesInfoList;
    private EventBus bus;
    private HashMap<String, BaseDevice> devices;
    private HashMap<String, ZigbeeGateway> gateways;

    public DeviceManager(String deviceInfoDir, EventBus bus) {
        this.deviceInfoDir = deviceInfoDir;
        this.gatewaysInfoList = new ArrayList<DeviceInfo>();
        this.devicesInfoList = new ArrayList<DeviceInfo>();
        this.bus = bus;
        this.deviceFactory = new DeviceFactory(new WatcherManager(this));
        this.devices = new HashMap<>();
        this.gateways = new HashMap<>();
    }

    public void loadDevice() {
        File devDir = new File(deviceInfoDir);
        if (!devDir.exists() && !devDir.isDirectory()) {
            LOGGER.log(Level.ALL, "Cannot access device dir : {0}", deviceInfoDir);
            return;
        }

        for (File devInfoFile : devDir.listFiles()) {
            if (!devInfoFile.getName().endsWith(".json"))
                continue;
            try {

                DeviceInfo deviceInfo = new Gson().fromJson(new FileReader(devInfoFile), DeviceInfo.class);
                deviceInfo.checkFields();

                String devType = deviceInfo.getType();
                if (devType != null && devType.equals("gateway")) {
                    if (gatewaysInfoList.contains(deviceInfo))
                        continue;
                    gatewaysInfoList.add(deviceInfo);
                } else {
                    if (devicesInfoList.contains(deviceInfo))
                        continue;
                    devicesInfoList.add(deviceInfo);
                }

            } catch (FileNotFoundException e) {
                LOGGER.log(Level.SEVERE, "Device info file {0} not found", devInfoFile.getName());
            } catch (JsonSyntaxException e) {
                LOGGER.log(Level.SEVERE, "Device info file parse error: {0}", devInfoFile.getName());
            } catch (VerifyError e) {
                LOGGER.log(Level.SEVERE,
                        String.format("Device info file parse error: %s : %s", devInfoFile.getName(), e.getMessage()));
            }
        }
    }

    public void setup() {
        setupGateways();
        setupDevices();
    }

    private void setupGateways() {
        for (DeviceInfo gatewayInfo : gatewaysInfoList) {
            LOGGER.log(Level.INFO, "load gateway: {0}", gatewayInfo.getSid());
            try {
                ZigbeeGateway gateway = deviceFactory.getGateway(gatewayInfo);
                addGateway(gatewayInfo.getSid(), gateway);
            } catch (DeviceNotSupported | DeviceNotDiscovered e) {
                LOGGER.warning(e.getMessage());
            }
        }

    }

    private void setupDevices() {
        for (DeviceInfo devInfo : devicesInfoList) {
            LOGGER.log(Level.INFO, String.format("load device: %s model : %s", devInfo.getSid(), devInfo.getModel()));
            try {
                BaseDevice device;
                if (devInfo.getArgs().containsKey("gateway")) {
                    String gatewaySid = devInfo.getArgs().get("gateway");
                    device = deviceFactory.getDevice(devInfo, this.getGateway(gatewaySid));
                } else {
                    device = deviceFactory.getDevice(devInfo);
                }
                addDevice(devInfo.getSid(), device);
            } catch (DeviceNotSupported e) {
                LOGGER.warning(e.getMessage());
            } catch (DeviceNotDiscovered e) {
                LOGGER.warning(e.getMessage());
            } catch (GatewayNotFound e) {
                LOGGER.warning(e.getMessage());
            }
        }
    }

    private synchronized void addGateway(String sid, ZigbeeGateway gateway) {
        this.gateways.put(sid, gateway);
    }

    private ZigbeeGateway getGateway(String sid) throws GatewayNotFound {
        if (!this.gateways.containsKey(sid)) {
            throw new GatewayNotFound(String.format("Gateway : %s not found", sid));
        }
        return this.gateways.get(sid);
    }

    private synchronized void addDevice(String sid, BaseDevice device) {
        this.devices.put(sid, device);
    }

    public void update(StatusEvent statusEvent) {
        BaseDevice dev = this.devices.get(statusEvent.getSid());
        if (dev != null) {
            try {
                if (dev.status.update(statusEvent)) {
                    bus.dispatch(statusEvent);
                }
            } catch (AttributeReadOnly e) {
                LOGGER.warning(String.format("Attribute %s is readonly", statusEvent.getName()));
            }
        }
    }

    public void execute(String sid, String cmd, Object args) {
        if (this.devices.containsKey(sid)) {
            BaseDevice device = this.devices.get(sid);
            device.execute(cmd, args);
        }
    }

}
