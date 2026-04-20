package com.kobosh.wurstaddon.client;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import com.kobosh.wurstaddon.client.hack.ExampleHack;
import com.kobosh.wurstaddon.client.hack.HackManager;

public class WurstaddonClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        // Register all hacks
        HackManager.registerHack(new ExampleHack());

        // Register tick event to update hacks every tick
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            HackManager.onTick();
        });

        // Example: Enable ExampleHack on client start (comment out if not needed)
        // HackManager.enableHack("Example Hack");
    }
}
