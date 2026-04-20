package com.kobosh.wurstaddon.client.hack;

import java.util.HashMap;
import java.util.Map;

/**
 * Manager for all hacks in WurstAddon
 */
public class HackManager {
    private static final Map<String, Hack> hacks = new HashMap<>();

    public static void registerHack(Hack hack) {
        hacks.put(hack.getName(), hack);
    }

    public static Hack getHack(String name) {
        return hacks.get(name);
    }

    public static Map<String, Hack> getAllHacks() {
        return new HashMap<>(hacks);
    }

    public static void enableHack(String name) {
        Hack hack = hacks.get(name);
        if (hack != null) {
            hack.setEnabled(true);
        }
    }

    public static void disableHack(String name) {
        Hack hack = hacks.get(name);
        if (hack != null) {
            hack.setEnabled(false);
        }
    }

    public static void onTick() {
        for (Hack hack : hacks.values()) {
            if (hack.isEnabled()) {
                hack.onTick();
            }
        }
    }
}
