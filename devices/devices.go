package devices

import (
	"homedaemon.angrysoft.ovh/homedaemon/discover"
	"homedaemon.angrysoft.ovh/homedaemon/status"
	"homedaemon.angrysoft.ovh/homedaemon/watcher"
)

type GatewayDevice interface {
	Setup(devInfo DeviceInfo, devDiscover *discover.DeviceDiscover, watcherManager *watcher.WatcherManager) error
	Send()
}

type Device interface {
	Setup(devInfo DeviceInfo, devDiscover *discover.DeviceDiscover, watcherManager *watcher.WatcherManager) error
}

type DeviceWithGateway interface {
	Setup(devInfo DeviceInfo, devDiscover *discover.DeviceDiscover, watcherManager *watcher.WatcherManager) error
	SetGateway(gate GatewayDevice)
}

type DeviceInfo struct {
	Sid         string            `json:"sid"`
	Type        string            `json:"type"`
	Manufacture string            `json:"manufacture"`
	Model       string            `json:"model"`
	Name        map[string]string `json:"name"`
	Place       map[string]string `json:"place"`
	Driver      DriverInfo        `json:"driver"`
	Args        map[string]string `json:"args"`
}

type DriverInfo struct {
	Name    string `json:"name"`
	Gateway string `json:"gateway"`
}

type BaseDevice struct {
	Status status.Status[any]
}

func (bd *BaseDevice) Sid() string {
	return bd.Status.Get("sid").(string)
}

func (bd *BaseDevice) CreateStatus(devInfo DeviceInfo) {
	bd.Status = *status.CreateStatus()
	bd.Status.RegisterAttribute("sid", devInfo.Sid)
	bd.Status.RegisterAttribute("place", devInfo.Place)
	bd.Status.RegisterAttribute("name", devInfo.Name)
}
