package discover

import "log"

type DeviceBaseInfo interface {
	Sid() string
	String() string
}

type DiscoverEngine interface {
	Search() ([]DeviceBaseInfo, error)
}

type DeviceDiscover struct {
	deviceCache map[string]DeviceBaseInfo
}


func (dd *DeviceDiscover) Discover(sid string, engine DiscoverEngine) DeviceBaseInfo {
	var result DeviceBaseInfo
	if devInfo, ok := dd.deviceCache[sid]; ok {
		result =  devInfo
	} 
	devices, err := engine.Search()
	if err != nil {
		log.Println(err)
		return result
	}
	for _, dev := range devices {
		dd.deviceCache[dev.Sid()] = dev
		if dev.Sid() == sid {
			result = dev
		}
	}
	return result
}