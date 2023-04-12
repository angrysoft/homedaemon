package ovh.angrysoft.homedaemon.watcher;

import java.time.LocalTime;

public class ClockWatcher extends Watcher {

    public ClockWatcher(String sid) {
        super(sid);
        //TODO Auto-generated constructor stub
    }

    @Override
    public void run() {
        LocalTime now = LocalTime.now();
        // TODO need implemetation
    }
    
}
