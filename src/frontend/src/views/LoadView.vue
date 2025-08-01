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
        <div class="back-button-fixed">
            <ZuruckButton />
        </div>
        <div class="tournament-list">
            <div
                v-for="tournament in tournaments"
                :key="tournament.id"
                class="tournament-item"
                @click="selectTournament(tournament)"
                :class="{
                    selected: selectedTournaments.includes(tournament.id),
                }"
            >
                {{ tournament.name || `Turnier #${tournament.id}` }}
            </div>
            <div v-if="tournaments.length === 0">
                <em>Keine Turniere gefunden.</em>
            </div>
        </div>

        <div class="action-buttons">
            <button
                v-if="!selectMode"
                class="delete-all-btn desktop-only"
                @click="enableSelectMode"
            >
                Turniere löschen
            </button>

            <div v-if="selectMode" class="selection-actions">
                <button class="cancel-btn" @click="cancelSelection">
                    Abbrechen
                </button>
                <button
                    class="confirm-delete-btn desktop-only"
                    @click="confirmDeleteSelected"
                    :disabled="selectedTournaments.length === 0"
                >
                    Ausgewählte löschen ({{ selectedTournaments.length }})
                </button>
                <button class="delete-all-btn" @click="confirmDeleteAll">
                    Alle löschen
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import ZuruckButton from "@/components/ZuruckButton.vue";

export default {
    name: "PreviousTournaments",
    components: {
        ZuruckButton,
    },
    data() {
        return {
            tournaments: [],
            selectMode: false,
            selectedTournaments: [],
            isDeleting: false,
        };
    },
    created() {
        this.fetchTournaments();
    },
    methods: {
        fetchTournaments() {
            // Prüfe, ob API-URL gesetzt ist (online)
            if (import.meta.env.VITE_API_URL) {
                axios
                    .get(`${import.meta.env.VITE_API_URL}/tournaments/`)
                    .then((response) => {
                        this.tournaments = response.data.tournaments || [];
                        // Speichere die komplette Liste im LocalStorage
                        localStorage.setItem(
                            "tournaments",
                            JSON.stringify(this.tournaments)
                        );
                    })
                    .catch(() => {
                        // Falls Fehler: versuche aus LocalStorage zu laden
                        const storedTournaments = localStorage.getItem("tournaments");
                        this.tournaments = storedTournaments
                            ? JSON.parse(storedTournaments)
                            : [];
                    });
            } else {
                // Offline: nur aus LocalStorage laden
                const storedTournaments = localStorage.getItem("tournaments");
                this.tournaments = storedTournaments
                    ? JSON.parse(storedTournaments)
                    : [];
            }
        },
        selectTournament(tournament) {
            if (!this.selectMode) {
                this.$router.push({
                    name: "TournamentPlan",
                    params: { id: tournament.id },
                });
                return;
            }

            const index = this.selectedTournaments.indexOf(tournament.id);
            if (index === -1) {
                this.selectedTournaments.push(tournament.id);
            } else {
                this.selectedTournaments.splice(index, 1);
            }
        },
        enableSelectMode() {
            this.selectMode = true;
            this.selectedTournaments = [];
        },
        cancelSelection() {
            this.selectMode = false;
            this.selectedTournaments = [];
        },
        confirmDeleteSelected() {
            if (this.selectedTournaments.length === 0) return;

            const count = this.selectedTournaments.length;
            if (
                confirm(
                    `Möchten Sie wirklich ${count} Turnier(e) löschen?\nDiese Aktion kann nicht rückgängig gemacht werden.`
                )
            ) {
                this.deleteTournaments(this.selectedTournaments);
            }
        },
        confirmDeleteAll() {
            if (this.tournaments.length === 0) return;

            if (
                confirm(
                    `Möchten Sie wirklich ALLE ${this.tournaments.length} Turniere löschen?\nDiese Aktion kann nicht rückgängig gemacht werden.`
                )
            ) {
                const allIds = this.tournaments.map((t) => t.id);
                this.deleteTournaments(allIds);
            }
        },
        async deleteTournaments(ids) {
            this.isDeleting = true;
            try {
                // Lösche jedes Turnier einzeln
                const deletePromises = ids.map((id) =>
                    axios.delete(
                        `${
                            import.meta.env.VITE_API_URL
                        }/tournaments/delete_plan/${id}`
                    )
                );

                // Warte auf alle Löschvorgänge
                await Promise.all(deletePromises);

                // Aktualisiere die Liste
                this.tournaments = this.tournaments.filter(
                    (t) => !ids.includes(t.id)
                );
                this.selectMode = false;
                this.selectedTournaments = [];
                alert(`${ids.length} Turnier(e) erfolgreich gelöscht`);
            } catch (error) {
                console.error("Fehler beim Löschen:", error);
                alert("Fehler beim Löschen der Turniere");
            } finally {
                this.isDeleting = false;
            }
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
    z-index: 1000;
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

.tournament-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 30px;
}

.tournament-item {
    padding: 15px 20px;
    font-size: 16px;
    background-color: #e0e0e0;
    border: 1px solid #999;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
}

.tournament-item:hover {
    background-color: #d5d5d5;
}

.tournament-item.selected {
    background-color: #ffcccc;
    border-color: #ff4444;
}

.action-buttons {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 20px;
}

.delete-all-btn {
    padding: 15px 20px;
    font-size: 16px;
    background-color: #ff4444;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    width: 100%;
}

.delete-all-btn:hover {
    background-color: #cc0000;
}

.selection-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.cancel-btn {
    padding: 15px 20px;
    font-size: 16px;
    background-color: #e0e0e0;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.confirm-delete-btn {
    padding: 15px 20px;
    font-size: 16px;
    background-color: #ff4444;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.back-button-fixed {
    position: fixed;
    left: 20px;
    bottom: 20px;
    transform: none;
    z-index: 1000;
}

.desktop-only {
    display: block;
}

@media screen and (max-width: 768px) {
    .desktop-only {
        display: none;
    }
    .button-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .button-item {
        justify-content: center !important;
    }

    .header {
        margin-bottom: 30px;
    }

    h1 {
        font-size: 20px;
        margin-bottom: 30px;
    }

    .logo {
        width: 70px;
    }
}
</style>
