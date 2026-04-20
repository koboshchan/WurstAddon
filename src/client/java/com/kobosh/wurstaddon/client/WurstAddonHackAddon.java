package com.kobosh.wurstaddon.client;

import net.wurstclient.addon.HackAddon;
import net.wurstclient.hack.Hack;
import com.kobosh.wurstaddon.client.hack.ExampleHack;

/**
 * WurstAddon HackAddon implementation for registering hacks with Wurst7
 */
public class WurstAddonHackAddon implements HackAddon {

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
}

