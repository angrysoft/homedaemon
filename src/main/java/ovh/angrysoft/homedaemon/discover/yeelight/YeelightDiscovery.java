package ovh.angrysoft.homedaemon.discover.yeelight;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.net.StandardSocketOptions;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.logging.Level;

import ovh.angrysoft.homedaemon.discover.DeviceDiscoverInfo;
import ovh.angrysoft.homedaemon.discover.DiscoverEngine;

public class YeelightDiscovery extends DiscoverEngine {
    public ArrayList<DeviceDiscoverInfo> search() {
        ArrayList<DeviceDiscoverInfo> results = new ArrayList<>();

        byte[] msgByte = "M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1982\r\nMAN: \"ssdp:discover\"\r\nST: wifi_bulb\r\n".getBytes();
        int port = 1982;
        String ip = "239.255.255.250";
        String ret = "";

        try (DatagramSocket udp = new DatagramSocket()) {
            udp.setSoTimeout(5000);
            udp.setOption(StandardSocketOptions.IP_MULTICAST_TTL, 32);
            DatagramPacket packet = new DatagramPacket(msgByte, msgByte.length);
            packet.setAddress(InetAddress.getByName(ip));
            packet.setPort(port);
            udp.send(packet);
            while (true) {
                byte[] buf = new byte[1024];
                DatagramPacket retPack = new DatagramPacket(buf, buf.length);
                udp.receive(retPack);
                ret += new String( retPack.getData(), StandardCharsets.UTF_8);
            }
        } catch (SocketTimeoutException e) {
        } catch (IOException e) {
            LOGGER.log(Level.ALL, "Search problem: {0}", e.toString());
        }
        
        for (String dev : ret.split("HTTP/1.1 200 OK\r\n")) {
            if (dev.length() == 0)
                continue;
            results.add(new YeelightDeviceInfo(dev));
        }

        return results;
    }
}