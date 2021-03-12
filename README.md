# Unifi Doorbell Bridge

I've recently purchased a Unifi doorbell and wasn't happy with the existing integration.

This is a work in progress but currently supports:
1) Telegram Integration: Message with photo when the doorbell is rung.
1) MQTT Message Sending: Message dispatched for Rings, Motion and Smart Detections of People
1) Standalone LIFX MQTT listener to blink the lights when the doorbell is rung.
1) Standalone Notifier listener to generate a GNOME notification when the doorbell is rung.
1) Remote logging to Grafana Loki.

Note: _The only feature that requires internet connectivity is the Telegram Bot interface, all other functionality can run locally on a LAN._

Obviously this is heavily customised for my existing use case, but I wanted to provide it as a starting point for others that may be wanting more from their doorbell. Pull requests for improved configurability are welcome!

The interface to the Doorbell is via the Unifi Protect `update` Websocket (for updates) and the direct http interface to the doorbell (for images).

**There is a massive debt of gratitude to the homebridge-unifi-protect project at https://github.com/hjdhjd/homebridge-unifi-protect/. Without this work it would have been much harder to implement this!**

## Requirements
All external requirements are somewhat optional, in that many can be disabled whilst maintaining other functionality. External services I have deployed are:
1) Grafana Loki for remote log aggregation. (_Really optional!_)
1) MQTT Server for GNOME and LIFX integration. (_Kind of optional!_)
1) Telegram for Telegram Notifications. (_Slightly optional..._)

## Installation
1) Setup Python Virtual Environment
1) Install Requirements
1) Copy:
    * `.secrets.example.toml` to `.secrets.toml`
    * `settings.example.toml` to `settings.toml`
    * `notifier_config.example.py` to `notifier_config.py` _**NOTE**: Only required for GNOME desktop notifications._

## Configuration
Edit the above files. Probably comment out things you don't have or want in your environment.

## Deployment
`systemd` can be used for deploying the `lifx_listener` and the `doorbell_bridge` code. Service file templates are included. This should run in a container, pull requests welcome!

`notifier_listener` is challenging to run in a virtual environment due to the using the `gi.repository`. I've intentionally removed the global configuration from this script so it can be run from the system python, with only the addition of the `paho-mqtt` package. 
