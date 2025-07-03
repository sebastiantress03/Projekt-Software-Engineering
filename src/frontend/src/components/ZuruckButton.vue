<template>
    <button @click="goBack" class="nav-button secondary">Zurück</button>
</template>

<script>
/**
 * @component ZuruckButton
 * @description
 * Ein Navigationsbutton, der zur vorherigen Seite oder einer definierten Route zurückführt.
 *
 * @props
 * (Keine)
 *
 * @emits click - Wird ausgelöst, wenn der Button geklickt wird.
 *
 * @example
 * <ZuruckButton />
 */
export default {
    name: "ZurueckButton",
    methods: {
        goBack() {
            const backRoute = this.$route.meta.backRoute || "/";
            this.$router.push(backRoute);
        },
    },
};
</script>

<style scoped>
/* Container-Layout */
.container {
    max-width: 500px;
    margin: 40px auto;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    text-align: center;
    position: relative;
    min-height: 80vh;
}

/* Basis-Styling für Navigationsbutton */
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
    background-color: #3d7a7a;
}

/* Positionierung des Zurück-Buttons */
.back-button-container {
    position: absolute;
    bottom: 20px;
    left: 20px;
}
.parent {
    transform: translate(0, 0);
}
</style>
