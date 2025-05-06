<template>
  <div class="plan">
    <h2>🗓️ Spielplan für Turnier #{{ tournamentId }}</h2>

    <div v-if="matches.length === 0">
      <p>Keine Spiele vorhanden.</p>
    </div>

    <div v-else>
      <div v-for="(match, index) in matches" :key="index" class="match-card">
        <p><strong>{{ match.match }}</strong></p>
        <p>🕒 {{ match.startTime }}</p>
        <p>🏟️ Feld: {{ match.field }}</p>
        <p>👥 Gruppe: {{ match.group }}</p>

        <!-- ✅ Spielstand-Eingabe -->
        <div class="score-entry">
          <label>Spielstand:</label>
          <input type="number" v-model.number="match.scoreA" min="0" />
          <span>:</span>
          <input type="number" v-model.number="match.scoreB" min="0" />
        </div>
      </div>
    </div>

    <div class="buttons">
      <button @click="goToNext">Weiter zur Auswertung</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TournamentPlan',
  props: ['id'],
  data() {
    return {
      matches: []
    }
  },
  computed: {
    tournamentId() {
      return this.id
    }
  },
  methods: {
    goToNext() {
      this.$router.push({ name: 'Evaluation' })
    }
  },
  mounted() {
    // 🔧 Dummy-Spiele mit Spielständen
    this.matches = [
      { match: 'Team A vs Team B', group: 'Gruppe 1', field: 1, startTime: '10:00', scoreA: null, scoreB: null },
      { match: 'Team C vs Team D', group: 'Gruppe 1', field: 2, startTime: '10:00', scoreA: null, scoreB: null },
      { match: 'Team A vs Team C', group: 'Gruppe 1', field: 1, startTime: '10:30', scoreA: null, scoreB: null },
      { match: 'Team B vs Team D', group: 'Gruppe 1', field: 2, startTime: '10:30', scoreA: null, scoreB: null }
    ]
  }
}
</script>

<style scoped>
.plan {
  max-width: 700px;
  margin: 40px auto;
  font-family: 'Segoe UI', sans-serif;
  color: #333;
}

.match-card {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  background: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.score-entry {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  font-weight: bold;
}

.score-entry input {
  width: 50px;
  padding: 6px;
  text-align: center;
  font-size: 16px;
}

.buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

button {
  padding: 10px 20px;
  background-color: #58aaa0;
  color: #cee9e6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #387d75;
}
</style>
