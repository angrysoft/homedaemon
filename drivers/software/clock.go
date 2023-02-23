package software

import (
	"homedaemon.angrysoft.ovh/homedaemon/devices"
	"homedaemon.angrysoft.ovh/homedaemon/discover"
	"homedaemon.angrysoft.ovh/homedaemon/watcher"
)


type Clock struct {
	
}

func (c *Clock) GetStatus() {

}

func (d *Clock) GetSid() string {
	return ""
}

func (d *Clock) Setup(devInfo devices.DeviceInfo, discover *discover.DeviceDiscover, watcher *watcher.WatcherManager) error {
	return nil
}