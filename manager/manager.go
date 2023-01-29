package manager

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"

	"homedaemon.angrysoft.ovh/homedaemon/devices"
	"homedaemon.angrysoft.ovh/homedaemon/drivers"
)

type DeviceManager struct {
	devices  map[string]devices.Device
	gateways map[string]devices.GatewayDevice
	dir      string
}

func New(devDir string) *DeviceManager {
	dev := &DeviceManager{
		dir:      devDir,
		devices:  make(map[string]devices.Device),
		gateways: make(map[string]devices.GatewayDevice),
	}
	dev.loadDevices()
	return dev
}

func (dm *DeviceManager) loadDevices() {
	gatewayList := []devices.DeviceInfo{}
	deviceList := []devices.DeviceInfo{}

	err := filepath.Walk(dm.dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if strings.HasSuffix(path, ".json") && !info.IsDir() {
			devInfo := &devices.DeviceInfo{}
			jsonFile, err := os.Open(path)
			if err != nil {
				log.Fatal(err)
			}
			defer jsonFile.Close()

			byteValue, _ := io.ReadAll(jsonFile)
			json.Unmarshal(byteValue, &devInfo)

			if devInfo.Type == "gateway" {
				gatewayList = append(gatewayList, *devInfo)
			} else {
				deviceList = append(deviceList, *devInfo)
			}

		}

		return nil
	})

	if err != nil {
		log.Fatal(err)
	}
	dm.setupGateways(gatewayList)
	dm.setupDevices(deviceList)
}

func (dm *DeviceManager) setupGateways(gatewayList []devices.DeviceInfo) {
	for _, devI := range gatewayList {
		dev, ok := drivers.GetGatewayDriver(devI)
		if !ok {
			log.Println("No driver for", devI.Model)
			continue
		}
		err := dev.Setup(devI)
		if err != nil {
			log.Println(err)
			continue
		}
		dm.gateways[devI.Sid] = dev
	}
}

func (dm *DeviceManager) setupDevices(deviceList []devices.DeviceInfo) {
	for _, devI := range deviceList {
		if gateSid := devI.Driver.Gateway; gateSid != "" {
			gate, ok := dm.getGateway(gateSid)
			if !ok {
				log.Println("No gateway for", devI.Sid, devI.Model)
				continue
			}
			dev, ok := drivers.GetDriverWithGateway(devI)
			if !ok {
				log.Println("No driver for", devI.Sid, devI.Model)
				continue
			}
			dev.SetGateway(gate)
			err := dev.Setup(devI)
			if err != nil {
				log.Println(err)
				continue
			}
			dm.devices[devI.Sid] = dev
		} else {
			dev, ok := drivers.GetDriver(devI)
			if !ok {
				log.Println("No driver for", devI.Sid, devI.Model)
				continue
			}
			dm.devices[devI.Sid] = dev
		}

	}
}

func (dm *DeviceManager) getGateway(sid string) (devices.GatewayDevice, bool) {
	result, ok := dm.gateways[sid]
	return result, ok
}

func (dm *DeviceManager) ListDevices() []devices.Device {
	result := []devices.Device{}
	for _, dev := range dm.devices {
		fmt.Println(dev)
		result = append(result, dev)
	}
	return result
}
