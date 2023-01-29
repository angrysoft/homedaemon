package bus

type Event struct {
	Topic string
	payload any
}

func NewEvent(subject string, args any) *Event {
	return &Event{
		Topic: subject,
		payload: args,
	}
}