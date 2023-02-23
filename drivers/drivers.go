package drivers

import (
	"fmt"

	"homedaemon.angrysoft.ovh/homedaemon/devices"
	"homedaemon.angrysoft.ovh/homedaemon/drivers/software"
	"homedaemon.angrysoft.ovh/homedaemon/drivers/yeelight"
)

func GetDriver(devInfo devices.DeviceInfo) (devices.Device, bool) {
	var dev devices.Device
	var ok bool = true
	switch devInfo.Model {
	case "Clock":
		fmt.Println(devInfo)
		dev = &software.Clock{}
	case "mono":
		dev = &yeelight.Mono{}
	case "desklamp":
		dev = &yeelight.DeskLamp{}
	case "color":
		dev = &yeelight.Color{}

	default:
		dev = nil
		ok = false
	}
	return dev, ok
}

func GetDriverWithGateway(devInfo devices.DeviceInfo) (devices.DeviceWithGateway, bool) {
	var dev devices.DeviceWithGateway
	var ok bool = true
	switch devInfo.Model {
	case "aaaa":
		dev = nil
	default:
		dev = nil
		ok = false
	}
	return dev, ok
}

func GetGatewayDriver(devInfo devices.DeviceInfo) (devices.GatewayDevice, bool) {
	var dev devices.GatewayDevice
	var ok bool = true
	switch devInfo.Model {
	case "zigbee2mqtt":
		dev = nil
	default:
		dev = nil
		ok = false
	}
	return dev, ok
}
