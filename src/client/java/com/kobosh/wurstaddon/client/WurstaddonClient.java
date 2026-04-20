package com.kobosh.wurstaddon.client;

import net.fabricmc.api.ClientModInitializer;

public class WurstaddonClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        // Hacks are registered via the HackAddon interface and ServiceLoader
        // No need for manual registration here
    }
}
