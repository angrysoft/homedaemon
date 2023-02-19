package discover

import (
	"errors"
	"fmt"
	"log"
	"net"
	"net/url"
	"strconv"
	"strings"
	"time"
)

type YeelightDeviceInfo struct {
	Id        string
	Power     bool
	Addr      string
	Model     string
	Support   []string
	Bright    int
	ColorMode int
	Ct        int
	Rgb       int
	Hue       int
	Sat       int
}

func (ydi *YeelightDeviceInfo) Sid() string {
	return ydi.Id
}

func (ydi *YeelightDeviceInfo) String() string {
	return fmt.Sprintf("%s : %s", ydi.Id, ydi.Addr)
}

type YeelightDiscover struct {
	addr          string
	searchRequest []byte
}

func NewYeelightDiscover() *YeelightDiscover {
	return &YeelightDiscover{
		addr:          "239.255.255.250:1982",
		searchRequest: []byte("M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1982\r\nMAN: \"ssdp:discover\"\r\nST: wifi_bulb\r\n"),
	}
}

func (y *YeelightDiscover) Search() ([]DeviceBaseInfo, error) {
	var result []DeviceBaseInfo
	ssdp, _ := net.ResolveUDPAddr("udp4", y.addr)
	conn, err := net.ListenUDP("udp4", ssdp)
	if err != nil {
		log.Println(err)
	}
	defer conn.Close()
	conn.WriteToUDP(y.searchRequest, ssdp)
	conn.SetReadDeadline(time.Now().Add(time.Second * 10))
	for {
		buff := make([]byte, 1024)
		size, _, err := conn.ReadFromUDP(buff)
		if err != nil {
			if e, ok := err.(net.Error); !ok || !e.Timeout() {
				return nil, errors.New("no devices found")
			}
			break
		}
		devInfo, ok := y.parseDev(buff, size)
		if ok {
			result = append(result, devInfo)
		}
	}
	return result, err
}

func (y *YeelightDiscover) parseDev(msg []byte, size int) (DeviceBaseInfo, bool) {
	ok := false
	result := &YeelightDeviceInfo{}
	info := string(msg)
	for _, line := range strings.Split(info, "\r\n") {
		if strings.ContainsRune(line, ':') {
			item := strings.SplitN(line, ":", 2)
			name := strings.TrimSpace(item[0])
			value := strings.TrimSpace(item[1])
			switch name {
			case "id":
				ok = true
				result.Id = value
			case "power":
				result.Power = value == "on"
			case "Location":
				addr, err := url.Parse(value)
				if err == nil {
					result.Addr = addr.Host
				}
			case "model":
				result.Model = value
			case "support":
				result.Support = strings.Split(value, " ")
			case "bright":
				result.Bright, _ = strconv.Atoi(value)
			case "color_mode":
				result.ColorMode, _ = strconv.Atoi(value)
			case "ct":
				result.Ct, _ = strconv.Atoi(value)
			case "rgb":
				result.Rgb, _ = strconv.Atoi(value)
			case "hue":
				result.Hue, _ = strconv.Atoi(value)
			case "sat":
				result.Sat, _ = strconv.Atoi(value)
			}
		}
	}
	return result, ok
}
