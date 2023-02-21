package watcher

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"reflect"
	"time"

	"homedaemon.angrysoft.ovh/homedaemon/bus"
)

type yeelightNotification struct {
	Method string      `json:"method"`
	Params paramValues `json:"params"`
}

type paramValues struct {
	Power     string `json:"power,omitempty"`
	Bright    int    `json:"bright,omitempty"`
	Ct        int    `json:"ct,omitempty"`
	Rgb       int    `json:"rgb,omitempty"`
	Hue       int    `json:"hue,omitempty"`
	Sat       int    `json:"sat,omitempty"`
	ColorMode int    `json:"color_mode,omitempty"`
	Flowing   int    `json:"flowing,omitempty"`
	DelayOff  int    `json:"delayoff,omitempty"`
}

type YeelightWatcher struct {
	addr string
	sid  string
}

func (yw *YeelightWatcher) Watch(ev chan<- *bus.Event) {
	conn, err := net.DialTimeout("tcp", yw.addr, time.Second*3)
	if err != nil {
		log.Println(err)
	}
	defer conn.Close()
	reader := bufio.NewReader(conn)
	for {
		data, err := reader.ReadString('\n')
		if err == nil {
			var notification *yeelightNotification
			err := json.Unmarshal([]byte(data), &notification)
			if err != nil {
				log.Println(err)
				continue
			}
			values := reflect.ValueOf(notification.Params)
			types := values.Type()
			for i := 0; i < values.NumField(); i++ {
				if values.Field(i).IsZero() {
					continue
				}
				topic := fmt.Sprintf("status.%s.%s.%v", yw.sid, types.Field(i).Name, values.Field(i))
				event := bus.NewEvent(topic, map[string]any{
					types.Field(i).Name : values.Field(i),
				})
				ev <- event
			}
		}
	}

}

func NewYeelightWatcher(sid, addr string) *YeelightWatcher {
	return &YeelightWatcher{
		sid:  sid,
		addr: addr,
	}
}
