package config

import (
	"testing"
)

func TestAdd(t *testing.T) {
	conf := New()
	conf.Set("mainCategory", "status", true)
}

func TestGet(t *testing.T) {
	conf := New()
	conf.Set("mainCategory", "status", true)
	value := conf.Get("mainCategory", "status")
	if value == nil {
		t.Error("Cannot get proper value")
	}
}

func TestGetCategory(t *testing.T) {
	conf := New()
	conf.Set("mainCategory", "status", true)
	category := conf.GetCategory("mainCategory")
	if category["status"] == nil {
		t.Error("wrong value")
	}
}
