# Changelog

## [0.3.4] - 2024-08-17

### Added

- Dockerfile

### Changed

- update dependencies

## [0.3.3] - 2024-04-14

### Added

- Device Driver [SONOFF SNZB-06P](src/main/java/ovh/angrysoft/homedaemon/devices/sonoff/zigbee/Snzb06P.java)
- New Traits OccupancySettingsTimeout, OccupancySettingsSensitive

### Changed

- Change item

## [0.3.2] - 2024-01-09

### Changed
 - zigbee2mqtt state_left etc to outlet

### Added
 - Device Driver [SONOFF SNZB-02D](src/main/java/ovh/angrysoft/homedaemon/devices/sonoff/zigbee/Snzb02D.java)

## [0.3.1] - 2024-01-04
- New Device Drivers SonOff [Tx Ultimate](https://sonoff.tech/product/smart-wall-switches/tx-ultimate/)
    - [T51C86](src/main/java/ovh/angrysoft/homedaemon/devices/sonoff/T51C86.java)
    - [T52C86](src/main/java/ovh/angrysoft/homedaemon/devices/sonoff/T52C86.java)
    - [T53C86](src/main/java/ovh/angrysoft/homedaemon/devices/sonoff/T53C86.java)
- Integration with ewelink Lan mode ( encrypt / decrypt)
- Base integration with ewelink cloud
- New Device Driver Sonoff mini (diy) [Mini](src/main/java/ovh/angrysoft/homedaemon/devices/sonoff/Mini.java)

## [0.2.0] - 2023-10-31

### Added

- New Device Driver [TS0011](src/main/java/ovh/angrysoft/homedaemon/devices/tuya/TS0011.java)
