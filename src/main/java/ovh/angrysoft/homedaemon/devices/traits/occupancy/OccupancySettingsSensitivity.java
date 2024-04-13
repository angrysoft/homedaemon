package ovh.angrysoft.homedaemon.devices.traits.occupancy;

public interface OccupancySettingsSensitivity<T> {
    T getOccupancySensitivity();

    void setOccupancySensitivity(T value);
}
