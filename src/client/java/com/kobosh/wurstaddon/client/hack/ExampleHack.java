package com.kobosh.wurstaddon.client.hack;

import net.minecraft.client.MinecraftClient;
import net.minecraft.text.Text;
import net.wurstclient.Category;
import net.wurstclient.hack.Hack;
import net.wurstclient.util.ChatUtils;

/**
 * Example hack that sends a message in chat and then disables itself
 */
public class ExampleHack extends Hack {

    public ExampleHack() {
        super("Example Hack");
        setCategory(Category.FUN);
    }

    @Override
    protected void onEnable() {
        ChatUtils.message("Example Hack enabled! This message will be sent once.");

        // Disable the hack after sending the message
        setEnabled(false);
    }

    @Override
    protected void onDisable() {
        // Cleanup if needed
    }
}
