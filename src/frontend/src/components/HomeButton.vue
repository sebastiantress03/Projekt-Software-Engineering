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
 * @component HomeButton
 * @description
 * Ein wiederverwendbarer Button mit konfigurierbarem Typ, Stil (Farbe, Größe) und deaktivierbarem Zustand.
 *
 * @props
 * @prop {String} type - Der Typ des Buttons (z. B. "button", "submit", "reset").
 * @prop {String} color - Die Farbklasse des Buttons (z. B. "primary", "secondary").
 * @prop {String} size - Die Größenklasse des Buttons (z. B. "normal", "large").
 * @prop {Boolean} disabled - Gibt an, ob der Button deaktiviert ist.
 *
 * @emits click - Wird ausgelöst, wenn der Button geklickt wird.
 *
 * @example
 * <HomeButton color="secondary" size="large" @click="handleClick">Klick mich</HomeButton>
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
/* Basis-Styling für den Button */
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
/* Farbvarianten */
.home-btn.primary {
    background-color: #387d75;
}
.home-btn.secondary {
    background-color: #00796b;
}
/* Deaktiviert */
.home-btn:disabled {
    background-color: #bbb;
    cursor: not-allowed;
}
/* Größenvarianten */
.home-btn.large {
    font-size: 20px;
    padding: 20px 40px;
}
</style>
