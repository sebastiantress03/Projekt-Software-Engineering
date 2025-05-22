<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="['home-btn', color, size]"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script>
/**
 * HomeButton
 * 
 * Ein wiederverwendbarer Button mit konfigurierbarem Typ, Stil (Farbe, Größe) und deaktivierbarem Zustand.
 * 
 * Emits:
 * - click: Wird ausgelöst, wenn der Button geklickt wird
 */
export default {
  name: "HomeButton",
  props: {
    /**
     * Der Typ des Buttons (z. B. "button", "submit", "reset")
     */
    type: { type: String, default: "button" },
    /**
     * Die Farbklasse des Buttons, z. B. "primary" oder "secondary"
     */
    color: { type: String, default: "primary" },
    /**
     * Die Größenklasse des Buttons, z. B. "normal" oder "large"
     */
    size: { type: String, default: "normal" },
    /**
     * Ob der Button deaktiviert ist
     */
    disabled: { type: Boolean, default: false },
  },
};
</script>

<style scoped>
.home-btn {
  background-color: #387d75;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  width: 220px;
  text-align: center;
}
.home-btn.primary {
  background-color: #387d75;
}
.home-btn.secondary {
  background-color: #00796b;
}
.home-btn:disabled {
  background-color: #bbb;
  cursor: not-allowed;
}
.home-btn.large {
  font-size: 20px;
  padding: 20px 40px;
}
</style>

