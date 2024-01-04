package ovh.angrysoft.homedaemon.discover.engines;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.net.StandardSocketOptions;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import ovh.angrysoft.homedaemon.discover.DiscoverEngine;

public class YeelightDiscoveryEngine extends DiscoverEngine {
    public Set<Map<String, Object>> search() {
        Set<Map<String, Object>> results = new HashSet<>();

        byte[] msgByte =
                "M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1982\r\nMAN: \"ssdp:discover\"\r\nST: wifi_bulb\r\n"
                        .getBytes();
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
                ret += new String(retPack.getData(), StandardCharsets.UTF_8);
            }
        } catch (SocketTimeoutException ignored) {
            LOGGER.log(Level.ALL, "Timeout: {0}", ignored.toString());
        } catch (IOException e) {
            LOGGER.log(Level.ALL, "Search problem: {0}", e.toString());
        } catch (IllegalArgumentException e) {
            LOGGER.warning(String.format("Error: %s - %s", e.toString(), e.getMessage()));

        }

        for (String dev : ret.split("HTTP/1.1 200 OK\r\n")) {
            if (dev.length() == 0)
                continue;
            Map<String, Object> deviceInfo = parseDevice(dev);
            synchronized (this) {
                results.add(deviceInfo);
            }
        }

        return results;
    }

    private Map<String, Object> parseDevice(String dev) {
        Map<String, Object> info = new HashMap<>();

        for (String line : dev.split("\r\n")) {
            if (!line.contains(":"))
                continue;
            String[] item = line.split(":", 2);
            String name = item[0].strip();
            String value = item[1].strip();
            switch (name) {
                case "id":
                    info.put("sid", value);
                    break;

                case "power":
                    info.put("power", value);
                    break;

                case "Location":
                    URI uri;
                    try {
                        uri = new URI(value.replace("yeelight", "http"));
                        info.put("addr", uri.getHost());
                        info.put("port", uri.getPort());
                    } catch (URISyntaxException e) {
                        e.printStackTrace();
                    }
                    break;

                case "model":
                    info.put("model", value);

                    break;

                case "support":
                    info.put("support", value.split(" "));
                    break;

                case "bright":
                    info.put("bright", Integer.parseInt(value));
                    break;

                case "color_mode":
                    info.put("colorMode", Integer.parseInt(value));
                    break;

                case "ct":
                    info.put("ct", Integer.parseInt(value));
                    break;

                case "rgb":
                    info.put("rgb", Integer.parseInt(value));
                    break;

                case "hue":
                    info.put("hue", Integer.parseInt(value));
                    break;

                case "sat":
                    info.put("sat", Integer.parseInt(value));
                    break;
                    
                default:
                    break;
            }
        }
        return info;
    }
}
