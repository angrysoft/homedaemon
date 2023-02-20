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

func NewWatcherManager() *WatcherManager {
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
		fmt.Println("Watcher: ", <-wm.events)
	}
}