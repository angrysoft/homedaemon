package yeelight

import (
	"fmt"
	"testing"
	"time"
)

const testAddr = "192.168.10.16:55443"

func TestYApiGetProp(t *testing.T) {
	api := newYeelightApi(testAddr)
	val, err := api.GetProp([]any{"bright"})
	if err != nil {
		t.Error(err)
	}
	_, ok := val["bright"]
	if !ok {
		t.Error("incorrect return value")
	}
	fmt.Println("value: ", val)
}

func TestYApiSetPower(t *testing.T) {
	api := newYeelightApi(testAddr)
	api.SetPower("on", 0)
	time.Sleep(1 * time.Second)
	api.SetPower("off", 0)

}
