package ovh.angrysoft.homedaemon.connections;

import java.io.IOException;
import java.net.StandardSocketOptions;

import ovh.angrysoft.homedaemon.exceptions.connctions.DeviceConnectionError;

public class UdpMulticastConnection extends UdpConnection {
    public UdpMulticastConnection() throws DeviceConnectionError {
        try {
            this.socket.setOption(StandardSocketOptions.IP_MULTICAST_TTL, 32);
        } catch (IOException e ) {
            throw new DeviceConnectionError("Create udp socket error: " + e);
        }
    }
    
}
