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

        <div class="tournament-list">
            <div 
                v-for="tournament in tournaments" 
                :key="tournament.id" 
                class="tournament-item"
                @click="selectTournament(tournament)"
                :class="{ 'selected': selectedTournaments.includes(tournament.id) }"
            >
                {{ tournament.name || `Turnier #${tournament.id}` }}
            </div>
            <div v-if="tournaments.length === 0">
                <em>Keine Turniere gefunden.</em>
                <div class="back-button-fixed">
                <ZuruckButton />
            </div>
            </div>
        </div>

        <div class="action-buttons">
            <button 
                v-if="!selectMode"
                class="delete-all-btn"
                @click="enableSelectMode"
            >
                Turniere löschen
            </button>
            
            <div v-if="selectMode" class="selection-actions">
                <button 
                    class="cancel-btn"
                    @click="cancelSelection"
                >
                    Abbrechen
                </button>
                <button 
                    class="confirm-delete-btn"
                    @click="confirmDeleteSelected"
                    :disabled="selectedTournaments.length === 0"
                >
                    Ausgewählte löschen ({{ selectedTournaments.length }})
                </button>
                <button 
                    class="delete-all-btn"
                    @click="confirmDeleteAll"
                >
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
            isDeleting: false
        };
    },
    created() {
        this.fetchTournaments();
    },
    methods: {
        fetchTournaments() {
            axios
                .get(`${import.meta.env.VITE_API_URL}/tournaments/`)
                .then((response) => {
                    this.tournaments = response.data.tournaments || [];
                })
                .catch(() => {
                    this.tournaments = [];
                });
        },
        selectTournament(tournament) {
            if (!this.selectMode) {
                this.$router.push({ name: "TournamentPlan", params: { id: tournament.id } });
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
            if (confirm(`Möchten Sie wirklich ${count} Turnier(e) löschen?\nDiese Aktion kann nicht rückgängig gemacht werden.`)) {
                this.deleteTournaments(this.selectedTournaments);
            }
        },
        confirmDeleteAll() {
            if (this.tournaments.length === 0) return;
            
            if (confirm(`Möchten Sie wirklich ALLE ${this.tournaments.length} Turniere löschen?\nDiese Aktion kann nicht rückgängig gemacht werden.`)) {
                const allIds = this.tournaments.map(t => t.id);
                this.deleteTournaments(allIds);
            }
        },
        async deleteTournaments(ids) {
        this.isDeleting = true;
    try {
        // Lösche jedes Turnier einzeln
            const deletePromises = ids.map(id => 
            axios.post(`${import.meta.env.VITE_API_URL}/tournaments/delete_plan/${id}`)
        );
        
        // Warte auf alle Löschvorgänge
        await Promise.all(deletePromises);
        
        // Aktualisiere die Liste
        this.tournaments = this.tournaments.filter(t => !ids.includes(t.id));
        this.selectMode = false;
        this.selectedTournaments = [];
        alert(`${ids.length} Turnier(e) erfolgreich gelöscht`);
    } catch (error) {
        console.error('Fehler beim Löschen:', error);
        alert('Fehler beim Löschen der Turniere');
    } finally {
        this.isDeleting = false;
    }
}
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

.ZuruckButton{

    position: bottom,left;
    bottom: 20px;
    left: 20px;
    z-index: 1000;
    
}

</style>
