package status

import (
	"errors"
)

type Status struct {
	attributes map[string]any
}

func CreateStatus() *Status {
	return &Status{
		attributes: make(map[string]any),
	}
}

func (s *Status) Len() int {
	return len(s.attributes)
}

func (s *Status) Get(name string) any {
	attr, ok := s.attributes[name]
	if !ok {
		return nil
	}
	return attr
}

func (s *Status) RegisterAttribute(name string, attr any) error {

	if _, ok := s.attributes[name]; ok {
		return errors.New("Attribute already registered")
	}
	s.attributes[name] = attr
	return nil
}

func (s *Status) UnregisterAttribute(name string) {
	delete(s.attributes, name)
}

// func (s *Status) AddAlias(aliasName, attrName string) error {
// 	_, ok := s.attributes[attrName]
// 	if ok {
// 		s.attributes[aliasName] = s.attributes[attrName]
// 	}
// 	return nil
// }
