package status

import "testing"

func TestNewAttribute(t *testing.T) {
	attr0 := NewBoolAttr(false)
	if attr0 == nil {
		t.Errorf("Attribute not created")
	}

	attr1 := NewStringAttr(false)
	if attr1 == nil {
		t.Errorf("Attribute not created")
	}

	if attr0.Value() != false {
		t.Errorf("Attribute attr0 has incorrect type")
	}

	if attr1.Value() != "" {
		t.Errorf("Attribute attr1 has incorrect type: %s", attr1.Value())
	}
}

func TestSetValue(t *testing.T) {
	attr0 := NewBoolAttr(false)
	attr0.SetValue(true)

	if power := attr0.Value(); !power {
		t.Error("set value failed")
	}

}

func TestReadOnlyAttr(t *testing.T) {
	attr0 := NewBoolAttr(true)
	err := attr0.SetValue(true)
	if err != nil || attr0.Value() != true {
		t.Errorf("%s", err)
	}

	err = attr0.SetValue(false)
	if err == nil {
		t.Errorf("error expected on set readonly attribute")
	}
}
