<template>
  <div class="plan">
    <div class="header">
      <img src="@/assets/STURA_HTWD_Logo.webp" alt="HTWD Stura Logo" class="logo" />
      <h2>Turnierplan</h2>
    </div>

    <div class="team-select">
      <label for="team">Wähle dein Team aus:</label>
      <select id="team" v-model="selectedTeam">
        <option disabled value="">-- bitte wählen --</option>
        <option v-for="team in allTeams" :key="team">{{ team }}</option>
      </select>
    </div>

    <div class="fields-scroll">
      <div
        v-for="(match, index) in matches"
        :key="index"
        class="match-card"
        :class="match.groupColor"
      >
        <p><strong>{{ match.match }}</strong></p>
        <p>🕒 {{ match.startTime }}</p>
        <p>🏟️ Feld: {{ match.field }}</p>
        <p>👥 Gruppe: {{ match.group }}</p>
        <p>⚖️ Schiedsrichter: {{ match.ref }}</p>

        <div class="score-entry" @click="openPopup(match)">
          <label>Spielstand:</label>
          <input type="number" :value="match.scoreA" readonly />
          <span>:</span>
          <input type="number" :value="match.scoreB" readonly />
        </div>
      </div>
    </div>

    <div class="buttons">
      <button @click="goToNext">Auswertung</button>
    </div>

    <!-- 📦 Popup -->
    <div v-if="showPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <h3>Ergebnis eintragen</h3>
        <p><strong>{{ currentMatch.match }}</strong></p>
        <p>Uhrzeit: {{ currentMatch.startTime }}</p>
        <div class="score-entry">
          <input type="number" v-model.number="currentMatch.scoreA" placeholder="Team A" />
          <span>:</span>
          <input type="number" v-model.number="currentMatch.scoreB" placeholder="Team B" />
        </div>
        <div class="popup-buttons">
          <button @click="closePopup">Abbrechen</button>
          <button @click="saveScore">Speichern</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TournamentPlan",
  props: ["id"],
  data() {
    return {
      selectedTeam: "",
      showPopup: false,
      currentMatch: null,
      allTeams: ["Team A", "Team B", "Team C", "Spätzünder", "Volleyboys"],
      matches: [],
    };
  },
  computed: {
    tournamentId() {
      return this.id;
    },
  },
  methods: {
    goToNext() {
      this.$router.push({ name: "Evaluation" });
    },
    openPopup(match) {
      this.currentMatch = match;
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
    },
    saveScore() {
      this.showPopup = false;
    },
  },
  mounted() {
    this.matches = [
      {
        match: "Funteam A vs Funteam B",
        group: "Fun",
        groupColor: "fun",
        field: 1,
        startTime: "14:00",
        ref: "Team 3",
        scoreA: null,
        scoreB: null,
      },
      {
        match: "Schwitzteam 1 vs Volleyboys",
        group: "Schwitzer",
        groupColor: "schwitzer",
        field: 1,
        startTime: "14:15",
        ref: "Team 2",
        scoreA: null,
        scoreB: null,
      },
      {
        match: "Schwitzteam 2 vs Funteam A",
        group: "Schwitzer",
        groupColor: "schwitzer",
        field: 1,
        startTime: "14:30",
        ref: "Team 1",
        scoreA: null,
        scoreB: null,
      },
    ];
  },
};
</script>

<style scoped>
.plan {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  font-family: "Segoe UI", sans-serif;
  color: #222;
  background: #f5f5f5;
  border-radius: 12px;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.logo {
  width: 80px;
  margin-bottom: 10px;
}

.team-select {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.team-select select {
  padding: 10px;
  font-size: 16px;
  margin-top: 8px;
  width: 250px;
}

.fields-scroll {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding-bottom: 10px;
}

.match-card {
  min-width: 260px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.match-card.fun {
  background-color: #e0f2f1;
}

.match-card.schwitzer {
  background-color: #fff3e0;
}

.score-entry {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  font-weight: bold;
  cursor: pointer;
}

.score-entry input {
  width: 50px;
  padding: 6px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
}

.buttons {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

button {
  padding: 10px 20px;
  background-color: #387d75;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #2d5f59;
}

/* 📦 Pop-up Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.popup {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.popup .score-entry {
  justify-content: center;
  margin: 15px 0;
}

.popup input {
  font-size: 16px;
}

.popup-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.popup-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.popup-buttons button:first-child {
  background-color: #ccc;
}

.popup-buttons button:last-child {
  background-color: #387d75;
  color: white;
}
</style>
