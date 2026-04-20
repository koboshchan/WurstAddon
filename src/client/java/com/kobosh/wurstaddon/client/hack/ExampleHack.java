package com.kobosh.wurstaddon.client.hack;

import net.minecraft.client.MinecraftClient;
import net.minecraft.text.Text;

/**
 * Example hack that sends a message in chat and then disables itself
 */
public class ExampleHack extends Hack {

    public ExampleHack() {
        super("Example Hack", "A simple example hack that sends hello world in chat");
    }

    @Override
    protected void onEnable() {
        // Send message in chat
        MinecraftClient client = MinecraftClient.getInstance();
        if (client.player != null) {
            client.player.sendMessage(Text.of("hello world"), false);
        }

        // Disable the hack after sending the message
        setEnabled(false);
    }

    @Override
    protected void onDisable() {
        // Cleanup if needed
    }
}
