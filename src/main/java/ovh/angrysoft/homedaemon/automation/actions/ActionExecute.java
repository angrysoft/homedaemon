package ovh.angrysoft.homedaemon.automation.actions;

import java.util.Optional;

import ovh.angrysoft.homedaemon.devices.DeviceManager;

public class ActionExecute extends Action {
    private String sid;
    private String cmd;
    private Optional<Object> arg;
    private DeviceManager deviceManager;
    private boolean runInBackground;

    public ActionExecute(String sid, String cmd, Optional<Object> arg, boolean runInBackground, DeviceManager deviceManager) {
        this.sid = sid;
        this.cmd = cmd;
        this.arg = arg;
        this.deviceManager = deviceManager;
    }

    public String getSid() {
        return sid;
    }

    public String getCmd() {
        return cmd;
    }

    public Object getArg() {
        return arg;
    }

    @Override
    public void run() {
        if (runInBackground) {
            new Thread(new Runnable() {

                @Override
                public void run() {
                    deviceManager.execute(sid, cmd, arg);
                }
            }).start();
            return;
        }
        deviceManager.execute(sid, cmd, arg);
    }
}
