<template>
    <div class="container">
        <h2>STURA HTWD Auswertung</h2>

        <header>
            <div class="logo-container">
                <img :src="sturaLogo" alt="STURA_HTWD_Logo" class="logo" />
            </div>
        </header>

        <div class="section">
            <label for="groupSelect">Leistungsgruppe: </label>
            <select id="groupSelect" v-model="selectedGroup">
                <option value="">-- Hier wählen --</option>
                <option v-for="group in groups" :key="group" :value="group">
                    {{ group }}
                </option>
            </select>
        </div>

        <div class="section">
            <h3>Gewinner:</h3>
            <div class="winner-box">
                <div v-if="winners.length">
                    <div v-for="winner in winners" :key="winner">
                        {{ winner }}
                    </div>
                </div>
                <div v-else>Bitte Leistungsgruppe wählen.</div>
            </div>
        </div>

        <div class="section">
            <h3>Ergebnisse:</h3>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Platzierung</th>
                            <th>Team</th>
                            <th>S</th>
                            <th>N</th>
                            <th>Punkte</th>
                            <th>G</th>
                            <th>Diff</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="row in results" :key="row.team">
                            <td>{{ row.platz }}</td>
                            <td>{{ row.team }}</td>
                            <td>{{ row.s }}</td>
                            <td>{{ row.n }}</td>
                            <td>{{ row.p }}</td>
                            <td>{{ row.g }}</td>
                            <td>{{ row.diff }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <button @click="goBack" class="back-button">
    <slot>Zurück</slot>
    </button>
    </div>
</template>

<script setup>

import ZuruckButton from "@/components/ZuruckButton.vue";
import { ref, computed, onMounted } from "vue";
import sturaLogo from "../assets/STURA_HTWD_Logo.webp";

const goBack = () => {
    window.history.length > 1 ? window.history.back() : window.location.href = '/';
};
// Beispiel: Matches aus LocalStorage oder API laden
const matches = ref([]);

// Beispiel: Teams pro Gruppe (kannst du auch dynamisch aus matches ableiten)
const groups = computed(() => {
    const groupSet = new Set(matches.value.map((m) => m.group));
    return Array.from(groupSet);
});

const selectedGroup = ref("");

// Hilfsfunktion: Tabelle für eine Gruppe berechnen
function calculateGroupTable(groupName) {
    // Teams der Gruppe extrahieren
    const teams = new Set();
    matches.value.forEach((m) => {
        if (m.group === groupName) {
            teams.add(m.teamA);
            teams.add(m.teamB);
        }
    });

    // Initialisiere Statistik für jedes Team
    const stats = {};
    teams.forEach((team) => {
        stats[team] = { team, s: 0, n: 0, p: 0, g: 0, diff: 0 };
    });

    // Spiele durchgehen und Statistik berechnen
    matches.value.forEach((m) => {
        if (m.group !== groupName) return;
        if (m.scoreA == null || m.scoreB == null) return; // Nur gewertete Spiele

        stats[m.teamA].g += m.scoreA;
        stats[m.teamB].g += m.scoreB;
        stats[m.teamA].diff += m.scoreA - m.scoreB;
        stats[m.teamB].diff += m.scoreB - m.scoreA;

        if (m.scoreA > m.scoreB) {
            stats[m.teamA].s += 1;
            stats[m.teamB].n += 1;
            stats[m.teamA].p += 3; // z.B. 3 Punkte für Sieg
        } else if (m.scoreA < m.scoreB) {
            stats[m.teamB].s += 1;
            stats[m.teamA].n += 1;
            stats[m.teamB].p += 3;
        } else {
            // Unentschieden (optional)
            stats[m.teamA].p += 1;
            stats[m.teamB].p += 1;
        }
    });

    // Sortiere nach Punkten, dann Differenz, dann erzielten Punkten
    const table = Object.values(stats).sort(
        (a, b) => b.p - a.p || b.diff - a.diff || b.g - a.g
    );

    // Platzierung vergeben
    table.forEach((row, i) => (row.platz = i + 1));

    // Gewinner bestimmen (alle mit Platz 1)
    const maxP = table[0]?.p ?? 0;
    const winners = table.filter((r) => r.p === maxP).map((r) => r.team);

    return { winners, results: table };
}

// Computed für aktuelle Auswahl
const winners = computed(() =>
    selectedGroup.value ? calculateGroupTable(selectedGroup.value).winners : []
);
const results = computed(() =>
    selectedGroup.value ? calculateGroupTable(selectedGroup.value).results : []
);

// Beispiel: Matches laden (hier aus LocalStorage, sonst aus API)
onMounted(() => {
    // Ersetze das durch deinen echten Datenbezug!
    const stored = localStorage.getItem("matches");
    if (stored) matches.value = JSON.parse(stored);
    // Oder: matches.value = await axios.get("/api/matches")
});

</script>

<style scoped>
.container {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 900px;
    margin: 0 auto;
    background-color: #fff;
}

h2 {
    color: #004d4d;
    text-align: center;
    margin-bottom: 10px;
}

.section {
    margin-bottom: 30px;
}

select {
    padding: 8px;
    font-size: 16px;
    width: 100%;
    max-width: 300px;
    margin-top: 5px;
}

.winner-box {
    background-color: #eee;
    padding: 10px;
    text-align: center;
    margin-top: 10px;
    border: 1px solid #ccc;
}

.table-wrapper {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 600px;
}

th,
td {
    border: 1px solid #999;
    padding: 8px;
    text-align: center;
    white-space: nowrap;
}

th {
    background-color: #006666;
    color: white;
}

.logo-container {
    display: flex;
    justify-content: center;
    margin: 15px 0;
}

.logo {
    max-width: 150px;
    height: auto;
}

.back-button {
    padding: 10px 20px;
    background-color: #006666;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

.back-button:hover {
    background-color: #008080;
}

.back-button-fixed {
    position: fixed;
    left: 20px;
    bottom: 20px;
    z-index: 1000;
}

.winner-row {
    background-color: #e6f7f5;
    font-weight: bold;
}

</style>
