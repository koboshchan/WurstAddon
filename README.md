# WurstAddon

## Overview

This project is a Wurst7 addon for Minecraft 1.21.1.

It uses Java ServiceLoader to register an addon provider that contributes hacks
to Wurst at startup.

## Current Example

`ExampleHack` demonstrates a minimal hack:

- Sends "hello world" when enabled.
- Disables itself immediately after running.

## How Addon Registration Works

1. Provider class: `WurstAddonHackAddon` implements `net.wurstclient.addon.Addon`.
2. Service file: `src/client/resources/META-INF/services/net.wurstclient.addon.Addon`.
3. Service file content points to the provider class.

No manual registration in `WurstaddonClient` is required.

## Build Requirements

1. Build Wurst first, either in:

   - `wurst7-base`, or
   - `../Wurst7`

2. Build this addon:

   - `./gradlew build`

`build.gradle` automatically resolves the newest matching Wurst jar from those
two locations.

## Validation

When Wurst starts, verify a log line similar to:

- `[Wurst] Loaded addon: WurstAddon (...)`

Then confirm `Example Hack` appears in the Wurst hack list and can be toggled.
