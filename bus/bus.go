package bus

type Bus struct {
	triggers map[uint32]Trigger
}

func New() *Bus {
	return &Bus{
		triggers: make(map[uint32]Trigger),
	}
}

func (b *Bus) AddTrigger(trigger Trigger) uint32 {
	var id uint32 = 0
	for {
		_, ok := b.triggers[id]
		if !ok {
			b.triggers[id] = trigger
			return id
		}
		id++
	}
}

func (b *Bus) DelTrigger(id uint32) {
	delete(b.triggers, id)
}

func (b *Bus) Emit(ev *Event) {
	for _, trigger := range b.triggers {
		if trigger.Compare(ev.topicList) {
			trigger.handler.Call(ev)
		}

	}
}
