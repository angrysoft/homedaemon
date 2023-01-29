package software

import "homedaemon.angrysoft.ovh/homedaemon/devices"

type Dummy struct {
}

func (d *Dummy) GetStatus() {

}

func (d *Dummy) GetSid() string {
	return ""
}

func (d *Dummy) Setup(devInfo devices.DeviceInfo) error {
	return nil
}
