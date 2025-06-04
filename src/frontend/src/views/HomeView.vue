<template>
  <div class="home">
    <div class="header">
  <img src="@/assets/STURA_HTWD_Logo.webp" alt="HTWD Stura Logo" class="logo" />

      <h1>Turnierorganisationssoftware</h1>
    </div>

    <div class="button-wrapper">
      <HomeButton @click="goToCreate" class="desktop-only">✏️ Turnier erstellen</HomeButton>
      <HomeButton @click="goToLoad">📁 Turnier laden</HomeButton>
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
  align-items: center;
  margin-bottom: 40px;
  gap: 20px;
}

.logo {
  width: 90px;
}

h1 {
  font-size: 24px;
  color: #222;
}

.button-wrapper {
  display: flex;
  flex-direction: row;
  gap: 30px;
}

/* In mobiler Ansicht: nur „Turnier laden“ sichtbar */
@media screen and (max-width: 768px) {
  .button-wrapper {
    flex-direction: column;
    gap: 20px;
  }

  .desktop-only {
    display: none;
  }

  h1 {
    font-size: 20px;
  }

  .logo {
    width: 70px;
  }
}
</style>
