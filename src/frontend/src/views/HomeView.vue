<template>
  <div class="home">
    <div class="header">
      <img src="@/assets/logo.svg" alt="HTW Stura Logo" class="logo" />
      <h1>Turnierorganisationssoftware</h1>
    </div>

    <div class="button-wrapper">
      <HomeButton @click="goToCreate">✏️ Turnier erstellen</HomeButton>
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
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
}

.logo {
  width: 90px;
}

h1 {
  font-size: 28px;
  color: #222;
}

.button-wrapper {
  display: flex;
  flex-direction: row;
  gap: 30px;
}
</style>
