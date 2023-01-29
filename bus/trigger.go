package bus

import "strings"

type Trigger struct {
	Topic string
	handler Handler
	topicList []string
}

func NewTrigger(topic string, handler Handler) *Trigger {
	return &Trigger{
		Topic: topic,
		handler: handler,
		topicList: strings.Split(topic, "."),
	}

}