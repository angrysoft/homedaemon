package ovh.angrysoft.homedaemon.discover;

import java.util.Set;
import java.util.logging.Logger;
import java.util.Map;



public abstract class DiscoverEngine {
    protected static DiscoverEngine instance;
    protected static final Logger LOGGER = Logger.getLogger("Homedaemon");

    protected DiscoverEngine() {

    }
    
    public abstract Set<Map<String, Object>> search();
}
