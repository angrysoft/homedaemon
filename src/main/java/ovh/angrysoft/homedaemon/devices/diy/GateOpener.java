package ovh.angrysoft.homedaemon.devices.diy;

import java.util.Optional;
import ovh.angrysoft.homedaemon.connections.HttpConnection;
import ovh.angrysoft.homedaemon.devices.BaseDevice;
import ovh.angrysoft.homedaemon.devices.DeviceInfo;
import ovh.angrysoft.homedaemon.devices.traits.openclose.Open;

public class GateOpener extends BaseDevice implements Open {
    private final HttpConnection httpConnection;
    private String ip;
    private int port;

    public GateOpener(DeviceInfo deviceInfo) {
        super(deviceInfo);
        this.httpConnection = new HttpConnection();
        this.ip = deviceInfo.getArgs().get("ip");
        this.port = deviceInfo.getArgs().get("port") != null
                ? Integer.parseInt(deviceInfo.getArgs().get("port")) : 80;
    }

    @Override
    public void doOpen() {
        String uriString = new StringBuilder().append("http://").append(ip).append(":").append(port)
                .append("/").append("open").toString();
        httpConnection.post(uriString, Optional.empty());
    }

    @Override
    public void setup() {
        // No setup needed for GateOpener
    }

}
