package ovh.angrysoft.homedaemon.connections;

import java.net.SocketException;
import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

public class UdpBroadcastConnection extends UdpConnection {
    public UdpBroadcastConnection() throws DeviceConnectionError {
        try {
            this.socket.setBroadcast(true);
        } catch (SocketException e ) {
            throw new DeviceConnectionError("Create udp socket error: " + e);
        }
    }
}
