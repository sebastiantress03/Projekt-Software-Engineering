<template>
    <button @click="$emit('click')" class="nav-button secondary">Zurück</button>
</template>

<script>
export default {
    name: 'ZurueckButton',
    methods: {
    goBack() {
      this.$router.push(''); // Navigieren zum beliebigen Ort
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
    background-color: #004d4d
;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.nav-button:hover {
    background-color: #3d7a7a;
}
</style>
