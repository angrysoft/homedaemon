package devices

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"
)

type DeviceManage struct {
	devices map[string]Device
	dir string
}

type driverInfo struct {
	Name string `json:"name"`
	Gateway string `json:"gateway"`
}

type Sid string

type DeviceInfo struct {
	Sid Sid `json:"sid"`
	Type string `json:"type"`
	Manufacture string `json:"manufacture"`
	Model string `json:"model"`
	Name map[string]string `json:"name"`
	Place map[string]string `json:"place"`
	Driver driverInfo `json:"driver"`
	Args map[string]string `json:"args"`

}

type Device interface {
	GetStatus()
	GetSid()
}


func CreateManager(devDir string) *DeviceManage {
	dev := &DeviceManage{
		dir: devDir,
		devices: make(map[string]Device),
	}
	dev.loadDevices()
	return dev
}


func (dm *DeviceManage) loadDevices() {
	err := filepath.Walk(dm.dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if strings.HasSuffix(path, ".json") && !info.IsDir() {
			devInfo := &DeviceInfo{}
			jsonFile, err := os.Open(path)
			if err != nil {
				log.Fatal(err)
			}
			defer jsonFile.Close()

			byteValue, _ := io.ReadAll(jsonFile)
			json.Unmarshal(byteValue, &devInfo)
			fmt.Println("Load Device", devInfo.Name["pl"], devInfo.Sid)
			// dev, ok := 
			// dm.devices[devInfo.sid] = 
		}
		return nil
	})

	if err != nil {
		log.Fatal(err)
	}
}

func (dm *DeviceManage) Query(sid string, parameter string) {

}

