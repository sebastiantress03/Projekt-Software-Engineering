<template>
  <div class="home">
    <h1>Turnierorganisationssoftware</h1>

    <div class="button-row">
      <button @click="goToCreate">Turnierplan erstellen</button>
      <button @click="goToLoad">Turnierplan laden</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    goToCreate() {
      this.$router.push('/create')
    },
    goToLoad() {
      this.$router.push('/load')
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  padding: 50px;
  font-family: Arial, sans-serif;
}

.button-row {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 40px;
}

button {
  padding: 20px 40px;
  font-size: 16px;
  cursor: pointer;
  background: #eee;
  border: 1px solid #ccc;
  transition: all 0.2s ease;
}

button:hover {
  background: #ddd;
}
</style>
