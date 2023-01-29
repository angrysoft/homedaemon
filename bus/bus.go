package bus

type Bus struct {
	triggers []Trigger
}

func New() *Bus {
	return &Bus{
		triggers: []Trigger{},
	}
}

func (b *Bus) AddTrigger(trigger Trigger) {
	b.triggers = append(b.triggers, trigger)
}

func (b *Bus) DelTrigger(trigger Trigger) {
	// for _, tr := range b.triggers {
	// 	if tr == trigger {

	// 	}
	// }
}

func (b *Bus) Emit(ev *Event) {
	triggers := b.getTriggers(ev.Topic)
	for _, trigger := range triggers {
		trigger.handler.Call(ev.payload)

	}
}

func (b *Bus) getTriggers(topic string) []Trigger {
	var triggers []Trigger
	for _, tr := range b.triggers {
		if tr.Topic == topic {
			triggers = append(triggers, tr)
		}
	}

	return triggers
}
