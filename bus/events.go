package bus

import "strings"

type Event struct {
	Topic string
	payload any
	topicList []string
}

func NewEvent(topic string, args any) *Event {
	return &Event{
		Topic: topic,
		payload: args,
		topicList: strings.Split(topic, "."),
	}
}