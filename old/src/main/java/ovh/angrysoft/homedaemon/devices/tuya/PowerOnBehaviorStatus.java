package ovh.angrysoft.homedaemon.devices.tuya;

public enum PowerOnBehaviorStatus {
    ON("on"),
    OFF("off"),
    PREVIOUS("previous");

    private final String state;

    PowerOnBehaviorStatus(final String state) {
        this.state = state;
    }

    @Override
    public String toString() {
        return this.state;
    }
}
