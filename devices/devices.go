package devices

type GatewayDevice interface {
	Setup(gateInfo DeviceInfo) error
	Send()
}

type Device interface {
	Setup(devInfo DeviceInfo) error
}

type DeviceWithGateway interface {
	Setup(devInfo DeviceInfo) error
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
}
