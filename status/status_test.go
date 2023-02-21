package status

import (
	"fmt"
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
	err = status.RegisterAttribute("place", )
	if err != nil && status.Len() != 1 {
		t.Error("Register attribute failed")
	}
}

func TestRegisterAlreadyRegisteredAttribute(t *testing.T) {
	status := CreateStatus()
	err := status.RegisterAttribute("power", false)
	if err != nil {
		t.Error("Register attribute failed")
	}
	err = status.RegisterAttribute("power", false)
	if err == nil && status.Len() > 1 {
		t.Error("Attribute re-registered")
	}
}

func TestUnregisterAttribute(t *testing.T) {
	status := CreateStatus()
	err := status.RegisterAttribute("power", false)
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
	st.RegisterAttribute("test", "some value")
	v := st.Get("test")
	fmt.Println(v)
	if v != "some value" {
		t.Error("incorrect value")
	}
}

func TestSet(t *testing.T) {
	st := CreateStatus()
	st.RegisterAttribute("test", "")
	st.Set("test", "other value")
	v := st.Get("test")
	if v != "other value" {
		t.Error("incorrect value")
	}
}

func TestAlias(t *testing.T) {
	status := CreateStatus()
	status.RegisterAttribute("power", "on")
	status.AddAlias("switch", "power")
	power := status.Get("power")
	fmt.Println(power)

	status.Set("switch", "off")
	sw := status.Get("switch")
	po := status.Get("power")
	fmt.Println(sw, po)
	if sw != po {
		t.Error("incorrect alias value")
	}

}

func TestUpdate(t *testing.T) {
	st := CreateStatus()
	st.RegisterAttribute("test", "some value")
	st.RegisterAttribute("power", false)
	newValues := map[string]any{
		"power": true,
		"test": "tset",
	}
	st.Update(newValues)
	v := st.Get("test")
	if v != "tset" {
		t.Error("incorrect value")
	}

	v = st.Get("power")
	if v != true {
		t.Error("incorrect value")
	}
}
