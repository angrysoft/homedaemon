package status

import "errors"

type AttrType interface {
	~int | ~string | ~bool
}

type Attributer[T AttrType] interface {
	SetValue(value T) error
	Value() T
}

type Attribute[T AttrType] struct {
	readonly    bool
	initialized bool
	value       T
}

func (a *Attribute[T]) SetValue(value T) error {
	if a.readonly {
		if a.initialized {
			return errors.New("read only parameter")
		}
		a.initialized = true
	}
	a.value = value
	return nil
}

func (a *Attribute[T]) Value() T {
	return a.value
}

func NewBoolAttr(readonly bool) *Attribute[bool] {
	return &Attribute[bool]{
		readonly: readonly,
		value:    false,
	}
}

func NewStringAttr(readonly bool) *Attribute[string] {
	return &Attribute[string]{
		readonly: readonly,
		value:    "",
	}
}
