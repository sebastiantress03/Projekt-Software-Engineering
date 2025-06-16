<template>
    <div class="container">
        <div class="logo-header">
            <img
                src="@/assets/STURA_HTWD_Logo.webp"
                alt="HTWD Stura Logo"
                class="logo"
            />
            <h2>Vorherige Turniere</h2>
        </div>

        <div class="tournament-buttons">
            <button
                v-for="tournament in tournaments"
                :key="tournament.id"
                class="tournament-btn"
                @click="goToPlan(tournament.id)"
            >
                {{ tournament.name || `Turnier #${tournament.id}` }}
            </button>
            <div v-if="tournaments.length === 0">
                <em>Keine Turniere gefunden.</em>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "PreviousTournaments",
    data() {
        return {
            tournaments: [],
        };
    },
    created() {
        axios
            .get(`${import.meta.env.VITE_API_URL}/tournaments/`)
            .then((response) => {
                // Die API liefert { tournaments: [...] }
                this.tournaments = response.data.tournaments || [];
            })
            .catch(() => {
                this.tournaments = [];
            });
    },
    methods: {
        goToPlan(id) {
            this.$router.push({ name: "TournamentPlan", params: { id } });
        },
    },
};
</script>

<style scoped>
.container {
    max-width: 500px;
    margin: 40px auto;
    padding: 20px;
    font-family: "Segoe UI", sans-serif;
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
