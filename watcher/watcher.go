package watcher

import (
	"homedaemon.angrysoft.ovh/homedaemon/bus"
)

type Watcher interface {
	Watch(ev chan<- *bus.Event)
}

type WatcherManager struct {
	watchers []Watcher
	events   chan *bus.Event
	handler  func(ev *bus.Event)
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

		// fmt.Println("Watcher: ", ev.Topic, ev)
		wm.handler(ev)
	}
}

func (wm *WatcherManager) SetHandler(handler func(ev *bus.Event)) {
	wm.handler = handler
}
