path = static
dart = dart2js -m -o
sasss = sassc -t compressed

all: alldart allcss

alldart: leds main rf rfpilot

leds: $(path)/leds.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

main: $(path)/main.dart
	$(dart) $(path)/main.dart.js $(path)/main.dart

rf: $(path)/rf.dart
	$(dart) $(path)/leds.dart.js $(path)/leds.dart

rfpilot: $(path)/rfpilot.dart
	$(dart) $(path)/rfpilot.dart.js $(path)/rfpilot.dart
	$(dart) $(path)/sw.dart.js $(path)/sw.dart

allcss: stylescss rfpilotcss

stylescss: $(path)/styles.css
	sassc -t compressed $(path)/styles.css $(path)/styles.min.css

rfpilotcss: $(path)/rfpilot.scss
	sassc -t compressed $(path)/rfpilot.scss $(path)/rfpilot.min.css
