<template>
  <div class="container">
    <div class="logo-header">
      <img src="@/assets/logo.svg" alt="HTW Stura Logo" class="logo" />
      <h2>Vorherige Turniere</h2>
    </div>

    <div class="tournament-buttons">
      <button class="tournament-btn" @click="goToPlan">Altes Turnier 1</button>
      <button class="tournament-btn" @click="goToPlan">Altes Turnier 2</button>
      <button class="tournament-btn" @click="goToPlan">Altes Turnier 3</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PreviousTournaments',
  methods: {
    goToPlan() {
      this.$router.push({ name: 'TournamentPlan' }); // Name aus deinem Router
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
  text-align: center;
}

.logo-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.logo {
  width: 80px;
  margin-bottom: 10px;
}

.tournament-buttons {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.tournament-btn {
  padding: 15px 20px;
  font-size: 16px;
  background-color: #e0e0e0;
  border: 1px solid #999;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.tournament-btn:hover {
  background-color: #d5d5d5;
}
</style>
