<template>
    <button @click="goBack" class="nav-button secondary">Zurück</button>
    
</template>

<script>
export default {
    name: 'ZurueckButton',
    methods: {
    goBack() {
    const backRoute = this.$route.meta.backRoute || '/';
    this.$router.push(backRoute);
    }
    }
};
</script>


<style scoped>

.container {
    max-width: 500px;
    margin: 40px auto;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
    text-align: center;
    position: relative;
    min-height: 80vh;
    
}

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

.back-button-container {
    position: absolute;
    bottom: 20px;
    left: 20px;
}
.parent {
    transform: translate(0, 0);
}
</style>
