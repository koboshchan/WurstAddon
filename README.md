# WurstAddon - Hack System

## Overview
This addon provides a simple hack system for WurstAddon. Hacks are features that can be enabled/disabled dynamically.

## ExampleHack

The **ExampleHack** is a simple demonstration hack that:
- Sends "hello world" in chat when enabled
- Automatically disables itself after sending the message

## How to Enable Hacks

### Option 1: Enable on Client Start
Edit [WurstaddonClient.java](../WurstaddonClient.java) and uncomment the line:
```java
HackManager.enableHack("Example Hack");
```

### Option 2: Using HackManager Programmatically
```java
HackManager.enableHack("Example Hack");
```

### Option 3: Add a Command (Future Enhancement)
You can create a command to enable/disable hacks at runtime.

## Creating Your Own Hack

1. Create a new class that extends `Hack`:
```java
public class MyHack extends Hack {
    public MyHack() {
        super("My Hack", "Description of my hack");
    }

    @Override
    protected void onEnable() {
        // Code to run when hack is enabled
    }

    @Override
    protected void onDisable() {
        // Code to run when hack is disabled
    }

    @Override
    public void onTick() {
        // Called every tick while enabled (optional)
    }
}
```

2. Register your hack in `WurstaddonClient.onInitializeClient()`:
```java
HackManager.registerHack(new MyHack());
```

## Files

- **Hack.java** - Base class for all hacks
- **ExampleHack.java** - Example implementation
- **HackManager.java** - Manages hack registration and lifecycle
