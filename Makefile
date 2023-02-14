run:
	go run homed.go

build:
	go build homed.go


all: build

tests: test_bus test_status

test_bus:
	go test -v ...bus

test_status:
	go test -v ...status