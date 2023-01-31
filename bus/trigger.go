package bus

import (
	"math"
	"strings"
)

type Trigger struct {
	Topic     string
	handler   Handler
	topicList []string
	Id        uint32
	wildCard  bool
}

func NewTrigger(topic string, handler Handler) *Trigger {
	trigger := &Trigger{
		Topic:     topic,
		handler:   handler,
		topicList: strings.Split(topic, "."),
		wildCard:  false,
	}
	for _, t := range trigger.topicList {
		if t == "*" {
			trigger.wildCard = true
		}
	}

	return trigger

}

func (t *Trigger) Compare(topicList []string) bool {
	triggerLength := len(t.topicList)
	topicListLength := len(topicList)
	if !t.wildCard && triggerLength != topicListLength {
		return false
	}
	maxLoop := uint(math.Min(float64(triggerLength), float64(topicListLength)))
	var i uint = 0
	for ;i < maxLoop;i++  {
		if t.topicList[i] == "*" {
			break
		}
		if t.topicList[i] != topicList[i] {
			return false
		}
	} 

	return true
}
