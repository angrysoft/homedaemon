package ovh.angrysoft.homedaemon.watcher;

import java.time.LocalTime;

import ovh.angrysoft.homedaemon.bus.Events.StatusEvent;

public class ClockWatcher extends Watcher {

    public ClockWatcher(String sid) {
        super(sid);
    }

    @Override
    public void run() {
        LocalTime now = LocalTime.now();
        while (now.getSecond() != 0) {
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            now = LocalTime.now();
        }

        while (true) {
            now = LocalTime.now();
            handler.call(new StatusEvent(sid, "time", String.format("%02d:%02d", now.getHour(), now.getMinute())));
            try {
                Thread.sleep(60000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }

}
