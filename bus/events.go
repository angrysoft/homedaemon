package bus

import (
	"fmt"
	"strings"
)

type Event struct {
	Topic string
	payload any
	topicList []string
}

func (e Event) String() string {
	return fmt.Sprintf("Topic: %s, payload: %s", e.Topic, e.payload)
}

func NewEvent(topic string, args any) *Event {
	return &Event{
		Topic: topic,
		payload: args,
		topicList: strings.Split(topic, "."),
	}
}