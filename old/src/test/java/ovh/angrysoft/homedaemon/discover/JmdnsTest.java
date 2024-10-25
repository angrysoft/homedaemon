package ovh.angrysoft.homedaemon.discover;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;

import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceListener;
import javax.jmdns.ServiceTypeListener;


public class JmdnsTest {

    private static class SampleListener implements ServiceListener {
        @Override
        public void serviceAdded(ServiceEvent event) {
            System.out.println("Service added: " + event.getInfo());
        }

        @Override
        public void serviceRemoved(ServiceEvent event) {
            System.out.println("Service removed: " + event.getInfo());
        }

        @Override
        public void serviceResolved(ServiceEvent event) {
            System.out.println("Service resolved: " + event.getInfo());
        }
    }

    public static void main(String[] args) throws InterruptedException {
        try {
            // Create a JmDNS instance
            JmDNS jmdns = JmDNS.create(InetAddress.getLocalHost());

            // Add a service listener
            jmdns.addServiceListener("_ewelink._tcp.local.", new SampleListener());

            // Wait a bit
            // Thread.sleep(3000);
            // jmdns.close();
        } catch (UnknownHostException e) {
            System.out.println(e.getMessage());
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}

class DiscoverServiceTypes {

    static class SampleListener implements ServiceTypeListener {

        @Override
        public void serviceTypeAdded(ServiceEvent event) {
            System.out.println("Service type added: " + event.getType());
        }

        /*
         * (non-Javadoc)
         * @see javax.jmdns.ServiceTypeListener#subTypeForServiceTypeAdded(javax.jmdns.ServiceEvent)
         */
        @Override
        public void subTypeForServiceTypeAdded(ServiceEvent event) {
            System.out.println("SubType for service type added: " + event.getType());
        }
    }

    /**
     * @param args
     *            the command line arguments
     */
    public static void main(String[] args) {
        /*
         * Activate these lines to see log messages of JmDNS Logger logger = LoggerFactory.getLogger(JmDNS.class); ConsoleHandler handler = new ConsoleHandler(); logger.addHandler(handler); logger.setLevel(Level.FINER);
         * handler.setLevel(Level.FINER);
         */

        try {
            JmDNS jmdns = JmDNS.create();
            jmdns.addServiceTypeListener(new SampleListener());
            Thread.sleep(5000);
            jmdns.close();
            System.out.println("Done");
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
