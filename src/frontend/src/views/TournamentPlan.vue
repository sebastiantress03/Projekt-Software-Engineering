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

        <div class="fields-grid">
            <div
                class="field-column"
                v-for="(matches, field) in groupMatchesByField(filteredMatches)"
                :key="field"
            >
                <div class="field-title">Feld {{ field }}</div>
                <MatchCard
                    v-for="match in matches"
                    :key="match.gameID"
                    :match="match"
                    @open-popup="openPopup"
                />
            </div>
        </div>

        <div class="buttons">
            <ExportButton />
            <HomeButton color="primary" @click="goToNext"
                >Auswertung</HomeButton
            >
        </div>

        <!-- Pop-up -->
        <div v-if="showPopup" class="popup-overlay" @click.self="closePopup">
            <div class="popup">
                <h3>Ergebnis eintragen</h3>
                <p>
                    <strong>{{ currentMatch.match }}</strong>
                </p>
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
                    <HomeButton color="secondary" @click="closePopup"
                        >Abbrechen</HomeButton
                    >
                    <HomeButton color="primary" @click="saveScore"
                        >Speichern</HomeButton
                    >
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
import ExportButton from "@/components/ExportButton.vue";

export default {
    name: "TournamentPlan",
    components: { MatchCard, HomeButton, ZuruckButton, ExportButton },
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
        filteredMatches() {
            if (!this.selectedTeam) return this.matches;
            return this.matches.filter(
                (m) =>
                    m.teamA === this.selectedTeam ||
                    m.teamB === this.selectedTeam ||
                    m.ref === this.selectedTeam
            );
        },
    },
    methods: {
        goToNext() {
            this.$router.push({ name: "Evaluation" });
        },
        goBack() {
            this.$router.go(-1);
        },
        openPopup(match) {
            this.currentMatch = { ...match };
            this.showPopup = true;
        },
        closePopup() {
            this.showPopup = false;
        },
        downloadCSV() {
            // CSV-Daten zusammenstellen, z.B. alle Matches exportieren
            if (!this.matches.length) {
                alert("Keine Spieldaten zum Exportieren vorhanden.");
                return;
            }

            const headers = [
                "Match",
                "Team A",
                "Team B",
                "Gruppe",
                "Spielfeld",
                "Startzeit",
                "Schiedsrichter",
                "Punkte Team A",
                "Punkte Team B",
            ];
            const rows = this.matches.map((m) => [
                `"${m.match}"`,
                `"${m.teamA}"`,
                `"${m.teamB}"`,
                `"${m.group}"`,
                `"${m.field}"`,
                `"${m.startTime}"`,
                `"${m.ref}"`,
                m.scoreA !== null ? m.scoreA : "",
                m.scoreB !== null ? m.scoreB : "",
            ]);

            let csvContent = headers.join(",") + "\n";
            rows.forEach((row) => {
                csvContent += row.join(",") + "\n";
            });

            const blob = new Blob([csvContent], {
                type: "text/csv;charset=utf-8;",
            });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);

            link.setAttribute("href", url);
            link.setAttribute(
                "download",
                `turnier_export_${this.id || "export"}.csv`
            );
            link.style.visibility = "hidden";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },

        async saveScore() {
            // Finde das Match im matches-Array und aktualisiere die Werte
            const idx = this.matches.findIndex(
                (m) => m.gameID === this.currentMatch.gameID
            );
            if (idx !== -1) {
                // Kopiere die Werte aus currentMatch zurück ins Array
                this.matches[idx].scoreA = this.currentMatch.scoreA;
                this.matches[idx].scoreB = this.currentMatch.scoreB;
            }
            // Speichere die aktualisierten Matches im localStorage
            localStorage.setItem("matches", JSON.stringify(this.matches));

            // Sende das Ergebnis ans Backend
            try {
                console.log("currentMatch:", this.currentMatch);
                await axios.put(
                    `${
                        import.meta.env.VITE_API_URL
                    }/tournaments/match_plan/match/${this.currentMatch.gameID}`,
                    {
                        score_team1: this.currentMatch.scoreA,
                        score_team2: this.currentMatch.scoreB,
                        time_change: new Date()
                            .toLocaleTimeString("de-DE", { hour12: false })
                            .slice(0, 5), // z.B. "14:23"
                    }
                );
            } catch (e) {
                alert("Fehler beim Speichern im Backend!");
            }

            this.showPopup = false;
        },
        extractTeamsFromMatches(matches) {
            // Extrahiere alle Teams aus team_names-Arrays
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
                gameID: m.game_id, // <-- Korrekt!
            }));
        },
        groupMatchesByField(matches) {
            const grouped = {};
            matches.forEach((m) => {
                if (!grouped[m.field]) grouped[m.field] = [];
                grouped[m.field].push(m);
            });
            return grouped;
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

            // Speichere die Matches im localStorage
            localStorage.setItem("matches", JSON.stringify(this.matches));
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

.fields-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    justify-content: center;
    margin-bottom: 30px;
}

.field-column {
    flex: 1 1 300px;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    background: #f9f9f9;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    box-sizing: border-box;
}

.field-title {
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
    color: #387d75;
    font-size: 18px;
}

.field-column > * {
    max-width: 100%;
    width: 100%;
    box-sizing: border-box;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 30px;
    flex-wrap: wrap;
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

.back-button-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.fixed-back-button {
    position: fixed;
    left: 20px;
    top: 20px;
    z-index: 1000;
    color: "primary";
}

@media (max-width: 768px) {
    .fields-grid {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
        flex-wrap: nowrap;
        width: 100vw;
        height: auto;
        gap: 0;
        justify-content: flex-start;
    }

    .field-column {
        flex: 0 0 100vw;
        scroll-snap-align: start;
        margin-left: auto;
        margin-right: auto;
        overflow-x: hidden;
    }

    .fixed-back-button {
        left: 10px;
        top: 10px;
    }
}
</style>

