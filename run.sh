#!/bin/bash

source .env
./gradlew bootRun --debug-jvm --args='--spring.profiles.active=dev'