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
	h := func(ev *Event) {
		fmt.Print(ev)
	}
	trig := NewTrigger("report.123341421.status.off", *NewHandler(h))
	bus.AddTrigger(*trig)
	if len(bus.triggers) != 1 {
		t.Errorf("Trigger not added")
	}
}

func TestDelTrigger(t *testing.T) {
	bus := New()
	h := func(ev *Event) {
		fmt.Print(ev)
	}
	trig := NewTrigger("report.123341421.status.off", *NewHandler(h))

	id := bus.AddTrigger(*trig)
	bus.DelTrigger(id)
	if len(bus.triggers) != 0 {
		t.Errorf("Trigger not deleted")
	}
}

func TestEmit(t *testing.T) {
	var result string
	h := func(ev *Event) {
		fmt.Print(ev)
		result = ev.payload.(string)
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

func TestEmitWildCard(t *testing.T) {
	var result string
	h := func(ev *Event) {
		fmt.Print(ev)
		result = ev.payload.(string)
	}

	bus := New()
	trig := NewTrigger("report.*", *NewHandler(h))
	bus.AddTrigger(*trig)
	bus.Emit(NewEvent("report.123341421.status.off", "status"))
	time.Sleep(100 * time.Millisecond)
	if result != "status" {
		t.Errorf("Handler not called")
	}
}
