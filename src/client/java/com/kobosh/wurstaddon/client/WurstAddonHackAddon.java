package com.kobosh.wurstaddon.client;

import net.wurstclient.addon.Addon;
import net.wurstclient.command.Command;
import net.wurstclient.hack.Hack;
import com.kobosh.wurstaddon.client.hack.ExampleHack;

/**
 * WurstAddon provider for registering hacks and commands with Wurst7.
 */
public class WurstAddonHackAddon implements Addon {

    private final Hack[] hacks = {
            new ExampleHack()
    };

    @Override
    public String getAddonName() {
        return "WurstAddon";
    }

    @Override
    public Hack[] getHacks() {
        return hacks;
    }

    @Override
    public Command[] getCommands() {
        return new Command[0];
    }
}
