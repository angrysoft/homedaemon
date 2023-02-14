package status

import (
	"fmt"
	"reflect"
	"testing"
)

func TestNewStatus(t *testing.T) {
	status := CreateStatus()
	if status == nil {
		t.Error("Status not created")
	}
}

func TestRegisterAttribute(t *testing.T) {
	status := CreateStatus()
	attr := NewBoolAttr(false)
	err := status.RegisterAttribute("power", attr)
	if err != nil && status.Len() != 1 {
		t.Error("Register attribute failed")
	}
}

func TestRegisterAlreadyRegisteredAttribute(t *testing.T) {
	status := CreateStatus()
	attr := NewBoolAttr(false)
	err := status.RegisterAttribute("power", attr)
	if err != nil {
		t.Error("Register attribute failed")
	}
	err = status.RegisterAttribute("power", attr)
	if err == nil && status.Len() > 1 {
		t.Error("Attribute re-registered")
	}
}

func TestUnregisterAttribute(t *testing.T) {
	status := CreateStatus()
	attr := NewBoolAttr(false)
	err := status.RegisterAttribute("power", attr)
	if err != nil {
		t.Error("Register attribute failed")
	}
	status.UnregisterAttribute("power")
	if status.Len() != 0 {
		t.Error("Unregistered failed")
	}
}

func TestGet(t *testing.T) {
	st := CreateStatus()
	strAttr := NewStringAttr(false)
	strAttr.SetValue("some value")
	st.RegisterAttribute("test", strAttr)
	v := st.Get("test")
	vof := reflect.ValueOf(v)
	fmt.Println(v.().Value(), vof.Type())
}

// func TestAlias(t *testing.T) {
// 	status := CreateStatus()
// 	attr := NewBoolAttr(false)
// 	status.RegisterAttribute("power", attr)
// 	status.AddAlias("switch", "power")
// 	if status.

// }
