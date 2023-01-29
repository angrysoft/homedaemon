package bus

import (
	"fmt"
	"testing"
	"time"
)

func TestNew(t *testing.T) {
	bus := New()
	if bus == nil {
		t.Errorf("New bus not created")
	}
}

func TestAddTrigger(t *testing.T) {
	bus := New()
	h := func(args any) {
		fmt.Print(args)
	}
	trig := NewTrigger("report.123341421.status.off", *NewHandler(h))
	bus.AddTrigger(*trig)
	if len(bus.triggers) != 1 {
		t.Errorf("Trigger not added")
	}
}

func TestDelTrigger(t *testing.T) {
	bus := New()
	h := func(args any) {
		fmt.Print(args)
	}
	trig := NewTrigger("report.123341421.status.off", *NewHandler(h))

	bus.AddTrigger(*trig)
	bus.DelTrigger(*trig)
	if len(bus.triggers) != 0 {
		t.Errorf("Trigger not deleted")
	}
}

func TestEmit(t *testing.T) {
	var result string
	h := func(args any) {
		fmt.Print(args)
		result = args.(string)
	}

	bus := New()
	trig := NewTrigger("report.123341421.status.off", *NewHandler(h))
	bus.AddTrigger(*trig)
	bus.Emit(NewEvent("report.123341421.status.off", "status"))
	time.Sleep(100 * time.Millisecond)
	if result != "status" {
		t.Errorf("Handler not called")
	}
}
