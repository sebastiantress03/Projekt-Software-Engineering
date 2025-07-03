<template>
    <button @click="$emit('click')" class="nav-button primary">Weiter</button>
</template>

<script>
/**
 * @component WeiterButton
 * @description
 * Ein Navigationsbutton, der einen Schritt im Formularprozess weiterführt.
 *
 * @props
 * (Keine)
 *
 * @emits click - Wird ausgelöst, wenn der Button geklickt wird.
 *
 * @example
 * <WeiterButton @click="goToNextStep" />
 */
export default {
    name: "WeiterButton",
    methods: {
        nextStep() {
            // Validierung der Pflichtfelder
            if (!this.form.tournament_name || this.form.number_of_fields < 1) {
                alert("Bitte füllen Sie alle Pflichtfelder aus!");
                return;
            }

            // Daten speichern (z. B. in Vuex oder Session)
            localStorage.setItem("tournamentData", JSON.stringify(this.form));

            // Navigation zum nächsten Schritt
            this.$router.push("/step2");
        },
    },
};
</script>

<style scoped>
/* Basis-Styling für Weiter-Button */
.nav-button {
    padding: 0.6rem 1.4rem;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    color: #cee9e6;
    background-color: #004d4d;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

/* Hover-Effekt */
.nav-button:hover {
    background-color: #006666;
}
</style>
