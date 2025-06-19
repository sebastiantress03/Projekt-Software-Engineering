<template>
    <button @click="$emit('click')" class="nav-button danger">Abbruch</button>
</template>

<script>
export default {
    name: 'AbbrechenButton',
    methods: {
    cancelTournament() {
    if (confirm('Möchten Sie wirklich abbrechen? Nicht gespeicherte Änderungen gehen verloren.')) {
      this.$router.push('/'); // Zurück zur HomeView
    }
    }
}
};
</script>

<style scoped>
.nav-button {
    padding: 0.6rem 1.4rem;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    color: #CEE9E6;
    background-color: #004d4d;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.nav-button:hover {
    background-color: #b34040;
}
</style>

