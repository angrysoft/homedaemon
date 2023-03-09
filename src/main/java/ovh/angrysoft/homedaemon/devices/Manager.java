package ovh.angrysoft.homedaemon.devices;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

public class Manager {
    private String deviceInfoDir;
    private static final Logger LOGGER = Logger.getLogger(Manager.class.getName());
    private ArrayList<DeviceInfo> gatewaysInfoList;
    private ArrayList<DeviceInfo> devicesInfoList;

    public Manager(String deviceInfoDir) {
        this.deviceInfoDir = deviceInfoDir;
        this.gatewaysInfoList = new ArrayList<DeviceInfo>();
        this.devicesInfoList = new ArrayList<DeviceInfo>();
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
                if (deviceInfo.type != null && deviceInfo.type.equals("gateway")) {
                    gatewaysInfoList.add(deviceInfo);
                } else {
                    devicesInfoList.add(deviceInfo);
                }

            } catch (FileNotFoundException e) {
                LOGGER.log(Level.ALL, "Device info file {0} not found", devInfoFile.getName());
            } catch (JsonSyntaxException e) {
                LOGGER.log(Level.ALL, "Device info file parse error: {0}", devInfoFile.getName());
            }
        }
    }

    public void setup() {
        setupGateways();
        setupDevices();
    }

    private void setupGateways() {
        for (DeviceInfo gatewayInfo : gatewaysInfoList) {
            LOGGER.log(Level.INFO, "load gateway: {0}", gatewayInfo.sid);
        }

    }

    private void setupDevices() {
        for (DeviceInfo devInfo : devicesInfoList) {
            LOGGER.log(Level.INFO, "load device: {0}", devInfo.sid);
        }
    }

    public BaseDevice getDriver(DeviceInfo deviceInfo) {
        return null;
    }
}
