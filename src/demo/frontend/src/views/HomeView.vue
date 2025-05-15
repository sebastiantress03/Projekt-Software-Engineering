<template>
    <div class="home">
        <h1>Turnierorganisationssoftware</h1>
        <div class="button-wrapper">
            <HomeButton @click="goToCreate">➕ Turnier erstellen</HomeButton>
            <HomeButton @click="goToLoad">📂 Turnier laden</HomeButton>
        </div>
    </div>
</template>

<script>
import HomeButton from "../components/HomeButton.vue";

export default {
    name: "HomeView",
    components: { HomeButton },
    methods: {
        goToCreate() {
            this.$router.push("/step1");
        },
        goToLoad() {
            this.$router.push("/load");
        },
    },
};
</script>

<style scoped>
.home {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #f9f9f9;
    font-family: "Segoe UI", sans-serif;
    padding: 20px;
}

h1 {
    font-size: 32px;
    margin-bottom: 50px;
    color: #222;
}

.button-wrapper {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>
