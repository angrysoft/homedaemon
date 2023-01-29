package software

import "homedaemon.angrysoft.ovh/homedaemon/devices"


type Clock struct {
	
}

func (c *Clock) GetStatus() {

}

func (d *Clock) GetSid() string {
	return ""
}

func (d *Clock) Setup(devInfo devices.DeviceInfo) error {
	return nil
}