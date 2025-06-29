<template>
  <div class="export-container">
    <HomeButton color="primary" @click="openExportDialog">Exportieren</HomeButton>
    
    <div v-if="showExportDialog" class="export-dialog">
      <div class="dialog-content">
        <h3>Turnier exportieren</h3>
        
        <div v-if="loading" class="loading-message">Lade Turnierliste...</div>
        <div v-else-if="loadingMatches" class="loading-message">Lade Spielpläne...</div>
        <div v-else-if="error" class="error-message">{{ error }}</div>
        <div v-else-if="tournaments.length === 0" class="empty-message">
          Keine Turniere verfügbar
        </div>
        <div v-else class="form-group">
          <label for="tournament-select">Turnier auswählen:</label>
          <select 
            id="tournament-select" 
            v-model="selectedTournament"
            @change="onTournamentSelect"
            class="tournament-select"
          >
            <option disabled value="">-- bitte wählen --</option>
            <option 
              v-for="tournament in tournaments" 
              :key="tournament.id" 
              :value="tournament"
            >
              {{ tournament.name }} (ID: {{ tournament.id }})
            </option>
          </select>

          <div v-if="selectedTournament?.matches" class="matches-info">
            <p>{{ selectedTournament.matches.length }} Spiele verfügbar</p>
          </div>
        </div>
        
        <div class="button-group">
          <HomeButton color="secondary" @click="closeExportDialog">Abbrechen</HomeButton>
          <HomeButton 
            color="primary" 
            @click="exportToCSV"
            :disabled="!selectedTournament || !selectedTournament.matches"
          >
            <span v-if="exporting">
              <i class="spinner"></i> Exportiere...
            </span>
            <span v-else>
              <i class="download-icon"></i> Als CSV exportieren
            </span>
          </HomeButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HomeButton from "@/components/HomeButton.vue";
import axios from "axios";

export default {
  name: "ExportButton",
  components: { HomeButton },
  data() {
    return {
      showExportDialog: false,
      tournaments: [],
      selectedTournament: null,
      loading: false,
      loadingMatches: false,
      exporting: false,
      error: null
    };
  },
  methods: {
    async openExportDialog() {
      this.showExportDialog = true;
      await this.fetchTournaments();
    },
    
    closeExportDialog() {
      this.showExportDialog = false;
      this.selectedTournament = null;
    },
    
    async fetchTournaments() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/tournaments/`);
        
        if (!response.data?.tournaments) {
          throw new Error("Ungültiges Datenformat erhalten");
        }
        
        this.tournaments = Array.isArray(response.data.tournaments) 
          ? response.data.tournaments.map(t => ({ 
              id: t.id,
              name: t.name,
              matches: null 
            }))
          : [];
          
      } catch (error) {
        console.error("Fehler beim Laden der Turniere:", error);
        this.error = "Turniere konnten nicht geladen werden: " + error.message;
      } finally {
        this.loading = false;
      }
    },
    
    async onTournamentSelect() {
      if (this.selectedTournament && !this.selectedTournament.matches) {
        this.loadingMatches = true;
        this.error = null;
        try {
          const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/tournaments/${this.selectedTournament.id}`
          );
          
          if (!response.data?.tournament) {
            throw new Error("Keine Spieldaten erhalten");
          }
          
          // Direkte Zuweisung statt $set
          this.selectedTournament.matches = Array.isArray(response.data.tournament) 
            ? response.data.tournament 
            : [];
          
        } catch (error) {
          console.error("Fehler beim Laden der Spiele:", error);
          this.error = "Spielplan konnte nicht geladen werden: " + error.message;
        } finally {
          this.loadingMatches = false;
        }
      }
    },
    
    async exportToCSV() {
      if (!this.selectedTournament?.matches) {
        alert("Keine Spieldaten zum Exportieren vorhanden");
        return;
      }
      
      this.exporting = true;
      
      try {
        const headers = [
          'Spiel ID', 'Gruppe', 'Team A', 'Team B',
          'Ergebnis', 'Schiedsrichter', 'Feld', 'Startzeit'
        ];
        
        const rows = this.selectedTournament.matches.map(match => {
          const teamA = match.team_names?.[0] || match.teamA || 'Unbekannt';
          const teamB = match.team_names?.[1] || match.teamB || 'Unbekannt';
          const referee = match.team_names?.[2] || match.ref || '-';
          const scoreA = match.scores?.[0] ?? match.scoreA ?? '';
          const scoreB = match.scores?.[1] ?? match.scoreB ?? '';
          const score = scoreA !== null && scoreB !== null ? `${scoreA}:${scoreB}` : "-:-";
          
          return [
            match.gameID || match.id || '',
            match.stage_name || match.group || '',
            `"${teamA}"`,
            `"${teamB}"`,
            score,
            `"${referee}"`,
            match.field || match.field_number || '',
            match.play_time || match.startTime || ''
          ].join(';');
        });
        
        const csvContent = [headers.join(';'), ...rows].join('\n');
        const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `turnier_${this.selectedTournament.name.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().slice(0,10)}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
      } catch (error) {
        console.error("Export fehlgeschlagen:", error);
        alert("Fehler beim Export: " + error.message);
      } finally {
        this.exporting = false;
      }
    }
  }
};
</script>

<style scoped>
.export-container {
  position: relative;
  display: inline-block;
}

.export-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background-color: white;
  padding: 25px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.tournament-select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.matches-info {
  margin-top: 10px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 20px;
}

.loading-message,
.error-message,
.empty-message {
  padding: 15px;
  margin: 15px 0;
  text-align: center;
  border-radius: 5px;
}

.loading-message {
  color: #1976d2;
  background-color: #e3f2fd;
}

.error-message {
  color: #d32f2f;
  background-color: #ffebee;
}

.empty-message {
  color: #757575;
  background-color: #f5f5f5;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>