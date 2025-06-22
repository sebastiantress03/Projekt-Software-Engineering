<template>
  <div class="plan">
    <div class="header">
      <img
        src="@/assets/STURA_HTWD_Logo.webp"
        alt="HTWD Stura Logo"
        class="logo"
      />
      <h2>Turnierplan</h2>
    </div>

    
    <div class="team-select" v-if="allTeams.length">
      <label for="team">Wähle dein Team aus:</label>
      <select id="team" v-model="selectedTeam">
        <option disabled value="">-- bitte wählen --</option>
        <option v-for="team in allTeams" :key="team">{{ team }}</option>
      </select>
    </div>

    <!-- Gruppierte Matches -->
    <div class="fields-scroll" v-if="matches.length">
      <div v-for="group in groupedMatches" :key="group.name" class="group-block">
        <div class="group-title">{{ group.name }}</div>
        <div class="group-matches">
          <div
            v-for="match in group.matches"
            :key="match.gameID"
            class="match-container"
          >
            <MatchCard :match="match" @open-popup="openPopup" />
          </div>
        </div>
      </div>
    </div>

    <div class="buttons">
      <HomeButton color="primary" @click="goToNext">Auswertung</HomeButton>
    </div>

    <!-- Pop-up -->
    <div v-if="showPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup">
        <h3>Ergebnis eintragen</h3>
        <p><strong>{{ currentMatch.match }}</strong></p>
        <p>Uhrzeit: {{ currentMatch.startTime }}</p>
        <div class="score-entry">
          <input
            type="number"
            v-model.number="currentMatch.scoreA"
            :placeholder="currentMatch.teamA"
          />
          <span>:</span>
          <input
            type="number"
            v-model.number="currentMatch.scoreB"
            :placeholder="currentMatch.teamB"
          />
        </div>
        <div class="popup-buttons">
          <HomeButton color="secondary" @click="closePopup">Abbrechen</HomeButton>
          <HomeButton color="primary" @click="saveScore">Speichern</HomeButton>
        </div>
      </div>
    </div>
    <div class="back-button-container">
      <ZuruckButton color="primary" @click="goBack">Zurück</ZuruckButton>
    </div>
  </div>
</template>

<script>
import MatchCard from "../components/MatchCard.vue";
import HomeButton from "../components/HomeButton.vue";
import axios from "axios";
import ZuruckButton from "@/components/ZuruckButton.vue";

export default {
  name: "TournamentPlan",
  components: { MatchCard, HomeButton, ZuruckButton },
  props: ["id"],
  data() {
    return {
      selectedTeam: "",
      showPopup: false,
      currentMatch: null,
      allTeams: [],
      matches: [],
    };
  },
  computed: {
    groupedMatches() {
      const groups = {};
      this.matches.forEach((match) => {
        if (!groups[match.group]) groups[match.group] = [];
        groups[match.group].push(match);
      });
      return Object.entries(groups).map(([name, matches]) => ({
        name,
        matches,
      }));
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
     goBack() {
    this.$router.go(-1); // Oder spezifische Route wie '/tournaments'
  },
    extractTeamsFromMatches(matches) {
      const teamSet = new Set();
      matches.forEach((m) => {
        if (Array.isArray(m.team_names)) {
          teamSet.add(m.team_names[0]);
          teamSet.add(m.team_names[1]);
        }
      });
      return Array.from(teamSet);
    },
    mapApiMatches(apiMatches) {
      return apiMatches.map((m) => ({
        match: `${m.team_names[0]} vs ${m.team_names[1]}`,
        teamA: m.team_names[0],
        teamB: m.team_names[1],
        group: m.stage_name,
        groupColor: m.stage_name?.toLowerCase() || "",
        field: m.field,
        startTime: m.play_time?.slice(0, 5) || "",
        ref: m.team_names[2] || "",
        scoreA: m.scores?.[0] ?? null,
        scoreB: m.scores?.[1] ?? null,
        gameID: m.gameID,
      }));
    },
  },
  async mounted() {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/tournaments/${this.id}`
      );
      const apiMatches = response.data.tournament || [];
      this.matches = this.mapApiMatches(apiMatches);
      this.allTeams = this.extractTeamsFromMatches(apiMatches);
    } catch (e) {
      this.matches = [];
      this.allTeams = [];
    }
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
  flex-direction: column;
  gap: 30px;
}

.group-title {
  font-weight: bold;
  font-size: 18px;
  padding: 8px 0;
  background-color: #f5f5f5;
  border-bottom: 2px solid #ccc;
}

.group-matches {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding-bottom: 10px;
}

.match-container {
  min-width: 260px;
}
.fixed-back-button {
  position: fixed;
  left: 20px;
  top: 20px;
  z-index: 1000;
  color: "primary";
}


@media (max-width: 768px) {
  .fixed-back-button {
    left: 10px;
    top: 10px;
  }
}

@media (max-width: 768px) {
  .group-matches {
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scroll-padding: 20px;
    padding-bottom: 20px;
  }

  .match-container {
    scroll-snap-align: center;
    flex: 0 0 85%;
  }
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

