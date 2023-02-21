package watcher

import (
	"fmt"

	"homedaemon.angrysoft.ovh/homedaemon/bus"
)

type Watcher interface {
	Watch(ev chan<- *bus.Event)
}

type WatcherManager struct {
	watchers []Watcher
	events chan *bus.Event
}

func New() *WatcherManager {
	return &WatcherManager{
		events: make(chan *bus.Event),
	}
}

func (wm *WatcherManager) RegisterWatcher(watcher Watcher) {
	wm.watchers = append(wm.watchers, watcher)
	go watcher.Watch(wm.events)
}


func (wm *WatcherManager) Run() {
	for {
		ev := <-wm.events
		
		fmt.Println("Watcher: ", ev.Topic, ev)
	}
}