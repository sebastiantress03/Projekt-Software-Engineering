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
                <option value="gruppe1">Leistungsgruppe 1</option>
                <option value="gruppe2">Leistungsgruppe 2</option>
                <option value="gruppe3">Leistungsgruppe 3</option>
                <option value="gruppe4">Leistungsgruppe 4</option>
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
</template>

<script setup>
import { ref, computed } from "vue";
import sturaLogo from "../assets/STURA_HTWD_Logo.webp";

const selectedGroup = ref("");
const dummyData = {
    gruppe1: {
        winners: ["Team Alpha", "Team Beta"],
        results: [
            {
                platz: 1,
                team: "Team Alpha",
                s: 10,
                n: 1,
                p: 130,
                g: 90,
                diff: 40,
            },
            {
                platz: 2,
                team: "Team Beta",
                s: 8,
                n: 3,
                p: 110,
                g: 95,
                diff: 15,
            },
        ],
    },
    gruppe2: {
        winners: ["Team Delta"],
        results: [
            {
                platz: 1,
                team: "Team Delta",
                s: 9,
                n: 2,
                p: 120,
                g: 80,
                diff: 40,
            },
            {
                platz: 2,
                team: "Team Omega",
                s: 7,
                n: 4,
                p: 100,
                g: 88,
                diff: 12,
            },
        ],
    },
};

const winners = computed(() => dummyData[selectedGroup.value]?.winners || []);
const results = computed(() => dummyData[selectedGroup.value]?.results || []);
</script>

<style scoped>
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}
h2 {
    color: #004d4d;
}
.section {
    margin-bottom: 30px;
}
select {
    padding: 5px;
    font-size: 16px;
}
.winner-box {
    background-color: #eee;
    padding: 10px;
    text-align: center;
    margin-top: 10px;
    border: 1px solid #ccc;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}
th,
td {
    border: 1px solid #999;
    padding: 8px;
    text-align: center;
}
th {
    background-color: #006666;
    color: white;
}
.logo-container {
    width: 100%;
    height: auto;
    overflow: hidden;
    display: flex;
    justify-content: center;
    background-color: var(--primary);
    padding: 15px 0;
}
.logo {
    max-width: 25%;
    height: auto;
    object-fit: contain;
}
</style>
