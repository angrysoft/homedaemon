package yeelight

import (
	"errors"

	"homedaemon.angrysoft.ovh/homedaemon/devices"
	"homedaemon.angrysoft.ovh/homedaemon/discover"
	"homedaemon.angrysoft.ovh/homedaemon/watcher"
)

type Mono struct {
	devices.BaseDevice
	api  yeelightApi
	addr string
}

func (m *Mono) Setup(devInfo devices.DeviceInfo, devDiscover *discover.DeviceDiscover, watcherManager *watcher.WatcherManager) error {
	m.CreateStatus(devInfo)
	m.Status.RegisterAttribute("addr", "")
	m.Status.RegisterAttribute("color_mode", 0)
	devDiscovered := devDiscover.Discover(devInfo.Sid, discover.NewYeelightDiscover())
	if devDiscovered == nil {
		return errors.New("discover device failed")
	}
	dev := devDiscovered.(*discover.YeelightDeviceInfo)
	m.addr = dev.Addr
	m.api = *newYeelightApi(dev.Addr)
	watcherManager.RegisterWatcher(watcher.NewYeelightWatcher(devInfo.Sid, dev.Addr))
	return nil
}

func (m *Mono) On() {
	m.api.On()
}

func (m *Mono) Off() {
	m.api.Off()
}
