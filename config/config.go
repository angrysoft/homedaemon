package config

import (
	"encoding/json"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"
)

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

type Config struct {
	data map[string]map[string]any
}

func New() *Config {
	config := &Config{
		data: make(map[string]map[string]any),
	}

	return config
}

func (c Config) Get(category, key string) any {
	return c.data[category][key]
}

func (c Config) GetCategory(key string) map[string]any {
	return c.data[key]
}

func (c Config) Set(category, key string, value any) {
	_, ok := c.data[category]
	if !ok {
		c.data[category] = make(map[string]any)
	} 
	c.data[category][key] = value
}

func (c Config) LoadFromDir(dirName string) {
	err := filepath.Walk(dirName, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if strings.HasSuffix(path, ".json") && !info.IsDir() {
			_, fileName := filepath.Split(path)
			name := strings.Split(fileName, ".")[0]
			
			var result map[string]any
			jsonFile, err := os.Open(path)
			if err != nil {
				log.Fatal(err)
			}
			defer jsonFile.Close()

			byteValue, _ := io.ReadAll(jsonFile)
			json.Unmarshal(byteValue, &result)
			c.data[name] = result
		}
		return nil
	})

	if err != nil {
		log.Fatal(err)
	}

}
