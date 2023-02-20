package main

/*
Copyright [2023] [Sebastian Zwierzchowski - Angrysoft <sebastian.zwierzchowski@gmail.com>]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import (
	"flag"
	"fmt"
	"log"
	"os"

	"homedaemon.angrysoft.ovh/homedaemon/config"
	"homedaemon.angrysoft.ovh/homedaemon/manager"
	"homedaemon.angrysoft.ovh/homedaemon/watcher"
)

const VERSION = "0.1.0"

func main() {
	conf := config.New()
	debug := flag.Bool("D", false, "Debug messages")
	devDir := flag.String("dev", "/etc/homedaemon/dev.d", "Path to devices dir")
	confDir := flag.String("conf", "/etc/homedaemon/conf.d", "Path to configs dir")
	showVersion := flag.Bool("version", false, "Print version number")
	flag.Parse()

	if *showVersion {
		fmt.Println("HomeDaemon version:", VERSION)
		os.Exit(0)
	}

	conf.LoadFromDir(*confDir)
	conf.Set("debug", "status", *debug)
	conf.Set("devDir", "path", *devDir)

	if id := conf.Get("homed", "id"); id == nil || id =="" {
		log.Fatal("Missing homeid value")
	}

	dm := manager.New(*devDir)
	dm.ListDevices()
	wm := watcher.NewWatcherManager()
	wm.RegisterWatcher(watcher.NewYeelightWatcher("0x0000000007200259", "192.168.10.16:55443"))
	wm.Run()
}
