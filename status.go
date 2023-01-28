package main

type Status struct {
	data map[string]map[string]any
}

func CreateStatus() *Status {
	return &Status{
		data: make(map[string]map[string]any),
	}
}

func (s *Status) Query(sid, parameter string) any {
	dev, ok := s.data[sid]
	if !ok {
		return nil
	}
	return dev[parameter]
}
