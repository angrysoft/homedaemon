package status

import (
	"errors"
)

type Status[T any] struct {
	attributes map[string]T
	aliases    map[string]string
}

func CreateStatus() *Status[any] {
	return &Status[any]{
		attributes: make(map[string]any),
		aliases:    make(map[string]string),
	}
}

func (s *Status[_]) Len() int {
	return len(s.attributes)
}

func (s *Status[T]) Get(name string) T {
	result, ok := s.attributes[name]
	if !ok {
		attrName, ok := s.aliases[name]
		if ok {
			result = s.attributes[attrName]
		}
	}
	return result
}

func (s *Status[T]) Set(name string, value T) {
	if _, ok := s.attributes[name]; ok {
		s.attributes[name] = value
	} else if attrName, ok := s.aliases[name]; ok {
		s.attributes[attrName] = value
	}
}

func (s *Status[T]) Update(value map[string]T) {
	for key, val := range(value) {
		s.Set(key, val)
	}
}

func (s *Status[T]) RegisterAttribute(name string, attr T) error {

	if _, ok := s.attributes[name]; ok {
		return errors.New("Attribute already registered")
	}
	s.attributes[name] = attr
	return nil
}

func (s *Status[_]) UnregisterAttribute(name string) {
	delete(s.attributes, name)
}

func (s *Status[_]) AddAlias(aliasName, attrName string) error {
	if _, ok := s.attributes[attrName]; ok {
		if _, ok := s.aliases[aliasName]; ok {
			return errors.New("Attribute already registered")
		}
		s.aliases[aliasName] = attrName
	}
	return nil
}
