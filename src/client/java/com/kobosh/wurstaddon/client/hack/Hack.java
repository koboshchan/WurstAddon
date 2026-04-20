package com.kobosh.wurstaddon.client.hack;

/**
 * Base class for all hacks/features in WurstAddon
 */
public abstract class Hack {
    private String name;
    private String description;
    private boolean enabled;

    public Hack(String name, String description) {
        this.name = name;
        this.description = description;
        this.enabled = false;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        if (enabled && !this.enabled) {
            this.enabled = true;
            onEnable();
        } else if (!enabled && this.enabled) {
            this.enabled = false;
            onDisable();
        }
    }

    /**
     * Called when the hack is enabled
     */
    protected abstract void onEnable();

    /**
     * Called when the hack is disabled
     */
    protected abstract void onDisable();

    /**
     * Called every game tick while the hack is enabled
     */
    public void onTick() {
    }
}
