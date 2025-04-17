<template>
  <div class="home">
    <h1>Turnierorganisationssoftware</h1>

    <div class="button-wrapper">
      <button @click="goToCreate">➕ Turnier erstellen</button>
      <button @click="goToLoad">📂 Turnier laden</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    goToCreate() {
      this.$router.push('/step1');
    },
    goToLoad() {
      this.$router.push('/load');
    }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f9f9f9;
  font-family: 'Segoe UI', sans-serif;
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

button {
  background-color: #387D75;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
  width: 220px;
  text-align: center;
}

button:hover {
  background-color: #1B423E;
  transform: scale(1.03);
}
</style>
