# WurstAddon - Hack System

## Overview
This addon integrates with Wurst7's hack system using the HackAddon interface and Java's ServiceLoader.

## ExampleHack

The **ExampleHack** is a simple demonstration hack that:
- Extends `net.wurstclient.hack.Hack` (from Wurst7)
- Sends "hello world" in chat when enabled
- Automatically disables itself after sending the message
- Shows up in the Wurst7 hack menu under the "Fun" category

## How Hacks Are Registered

1. **HackAddon Implementation** - `WurstAddonHackAddon.java` implements the `HackAddon` interface and provides all hacks
2. **ServiceLoader** - The file `META-INF/services/net.wurstclient.addon.HackAddon` registers the addon with Wurst7
3. **Automatic Discovery** - When Wurst7 loads, it uses Java's ServiceLoader to discover and load all registered addons

## Creating Your Own Hack

1. Create a new class that extends `net.wurstclient.hack.Hack`:
```java
import net.wurstclient.Category;
import net.wurstclient.hack.Hack;

public class MyHack extends Hack {
    public MyHack() {
        super("My Hack");
        setCategory(Category.FUN);  // Or other category
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
        // Optional: Called every tick while enabled
    }
}
```

2. Add your hack to `WurstAddonHackAddon.java`:
```java
private final Hack[] hacks = {
    new ExampleHack(),
    new MyHack()  // Add your hack here
};
```

## Available Categories

- `Category.BLOCKS`
- `Category.MOVEMENT`
- `Category.COMBAT`
- `Category.RENDER`
- `Category.CHAT`
- `Category.FUN`
- `Category.ITEMS`
- `Category.OTHER`

## Dependencies

This addon depends on:
- Wurst7 (for the hack framework)
- Fabric API (for basic fabric mod functionality)

## Files

- **ExampleHack.java** - Example hack implementation
- **WurstAddonHackAddon.java** - HackAddon provider
- **META-INF/services/net.wurstclient.addon.HackAddon** - ServiceLoader configuration

