<template>
    <div class="home">
        <div class="header">
            <img
                src="@/assets/STURA_HTWD_Logo.webp"
                alt="HTWD Stura Logo"
                class="logo"
            />
            <h1>Turnierorganisationssoftware</h1>
        </div>

        <div class="button-grid">
            <div class="button-item left-button desktop-only">
                <HomeButton @click="goToCreate"
                    >Turnierplan erstellen</HomeButton
                >
            </div>

            <div class="button-item right-button">
                <HomeButton @click="goToLoad">Turnierplan laden</HomeButton>
            </div>
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
    text-align: center;
}

.header {
    display: flex;
    flex-direction: column;
    margin-bottom: 40px;
    gap: 15px;
    align-items: center; /* vertikal zentrieren */
    gap: 1rem;
}

.logo {
    width: 90px;
}

h1 {
    font-size: 24px;
    color: #222;
    font-weight: bold;
    margin-bottom: 50px;
}

.button-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    width: 100%;
    max-width: 800px;
}

.button-item {
    display: flex;
    align-items: center;
    gap: 15px;
}

.left-button {
    justify-content: flex-end;
}

.right-button {
    justify-content: flex-start;
}

.desktop-only {
    display: flex;
}

@media screen and (max-width: 768px) {
    .desktop-only {
        display: none;
    }
    .button-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .button-item {
        justify-content: center !important;
    }

    .header {
        margin-bottom: 30px;
    }

    h1 {
        font-size: 20px;
        margin-bottom: 30px;
    }

    .logo {
        width: 70px;
    }
}
</style>
