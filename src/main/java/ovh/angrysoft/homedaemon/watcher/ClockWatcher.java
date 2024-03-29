package ovh.angrysoft.homedaemon.watcher;

import java.time.LocalTime;

import ovh.angrysoft.homedaemon.bus.Event;

public class ClockWatcher extends Watcher {

    public ClockWatcher(String sid) {
        super(sid);
    }

    @Override
    public void run() {

        while (true) {
            LocalTime now = LocalTime.now();
            handler.call(Event.timeEvent("time",
                    String.format("%02d:%02d:%02d", now.getHour(), now.getMinute(), now.getSecond())));
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }

}
