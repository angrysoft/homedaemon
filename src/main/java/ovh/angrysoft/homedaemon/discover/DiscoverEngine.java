package ovh.angrysoft.homedaemon.discover;

import java.util.ArrayList;
import java.util.logging.Logger;



public abstract class DiscoverEngine {
    protected static final Logger LOGGER = Logger.getLogger("Homedaemon");
    
    public abstract ArrayList<DeviceDiscoverInfo> search();
}
