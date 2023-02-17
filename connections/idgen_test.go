package connections

import "testing"

func TestIdGen(t *testing.T) {
	id := &IdGen{}
	i := id.GetId()
	if i != 1 {
		t.Error("wrong Id")
	}
	i = id.GetId()
	if i != 2 {
		t.Error("wrong Id")
	}
}

func TestMaxId(t *testing.T) {
	id := &IdGen{
		current : 1000,
	}
	i := id.GetId()
	if i != 1 {
		t.Error("wrong id")
	}
}