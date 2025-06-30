# Tournament Management System - Comprehensive Documentation

## Inhaltsverzeichnis
1. [Systemübersicht](#system-uebersicht)
2. [Komponentendokumentation](#komponentendokumentation)
   - [TurnierErstellen](#turnier-erstellen)
   - [TurnierAuswertung](#turnier-auswertung)
   - [TurnierPlan](#turnier-plan)
   - [VorherigeTurniere](#vorherige-turniere)
   - [TurnierErstellungsschritte](#turnier-erstellungsschritte)
3. [API-Dokumentation](#api-dokumentation)
4. [Styleguide](#styleguide)
5. [Entwicklungsanleitung](#entwicklungsanleitung)


## Systemübersicht <a name="system-uebersicht"></a>
Eine umfassende Vue.js-Anwendung zur Verwaltung von Sportturnieren mit Funktionen für:
- Turniererstellung und -konfiguration
- Spielplanung
- Ergebnisverfolgung und -auswertung
- Teammanagement

## Komponentendokumentation <a name="komponentendokumentation"></a>

### TurnierErstellen <a name="turnier-erstellen"></a>
**Datei:** `/views/CreateTournament.vue`  
**Zweck:** Komplette Oberfläche zur Turniererstellung

#### Datenstruktur
```javascript
{
  tournament_name: "",       // Pflichtfeld
  number_of_fields: 1,       // Minimum: 1
  return_match: "true",      // "true" oder "false"
  time_to_start: "09:00",    // Format: HH:mm
  game_time: 10,             // Minuten
  warm_up_time: 5,           // Minuten
  number_of_breaks: 1,       // Anzahl Pausen
  break_length: [5],         // Minuten pro Pause
  break_times: [""],         // Startzeiten (HH:mm)
  stage_name: ["Gruppe A"],  // Gruppennamen
  number_of_teams: [4]       // Teams pro Gruppe
}
```
### Methoden

| Methode | Parameter | Beschreibung |
|---------|-----------|--------------|
| `updateStages` | Keine | Aktualisiert die Gruppenliste bei Änderung der Gruppenanzahl |
| `updateBreaks` | Keine | Aktualisiert die Pausenliste bei Änderung der Pausenanzahl |
| `submit` | Keine | Validiert das Formular und gibt die Daten in der Konsole aus ||


### TurnierAuswertung <a name="turnier-auswertung"></a>
**Datei:** `/views/Evaluation.vue`  
**Zweck:** Zeigt Turnierergebnisse und Gewinner an

#### Dynamische Eigenschaften
| Eigenschaft | Typ | Beschreibung |
|-------------|-----|--------------|
| `selectedGroup` | String | Aktuell ausgewählte Gruppe |
| `winners` | Computed<String[]> | Liste der Gewinner für die ausgewählte Gruppe |
| `results` | Computed<Object[]> | Spielergebnisse für die ausgewählte Gruppe |

#### Testdatenstruktur
```javascript
{
  [gruppenName]: {
    winners: ["Team Alpha", "Team Beta"],
    results: [
      {
        platz: 1,           // Position
        team: "Team Alpha", // Teamname
        s: 10,              // Siege
        n: 1,               // Niederlagen
        p: 130,             // Punkte
        g: 90,              // Gegentore
        diff: 40            // Tordifferenz
      }
    ]
  }
}
```

## TurnierPlan <a name="turnierplan"></a>
**Datei:** `/views/TournamentPlan.vue`  
**Zweck:** Anzeige des Spielplans und Ergebnis-Eingabe

### Hauptfunktionen
- Interaktive Spielkarten mit Teaminformationen
- Ergebnis-Eingabe über Modal-Popup
- Teamauswahl-Dropdown
- Visuelle Gruppierung nach Spielfeldern

### API-Integration
```javascript
// Turnierdaten laden
GET /tournaments/:id

// Spielergebnis aktualisieren
PUT /tournaments/match_plan/match/:gameID
```


## VorherigeTurniere <a name="vorherige-turniere"></a>
**Datei:** `/views/PreviousTournaments.vue`  
**Zweck:** Anzeige gespeicherter Turniere

### Datenfluss
| Schritt | Aktion |
|---------|--------|
| 1 | Lädt Turnierliste von der API |
| 2 | Zeigt sie als interaktive Buttons an |
| 3 | Bei Auswahl Navigation zur TurnierPlan-Ansicht |

## LoescheButton  
**Datei:** `/components/LoescheButton.vue`  
**Zweck:** Generischer Löschbutton-Komponente für einzelne Elemente (z. B. Turniere)

```vue
<template>
  <button class="delete-btn" @click="handleDelete">
    Löschen
  </button>
</template>

<script>
import axios from "axios";

export default {
  name: "LoescheButton",
  props: {
    id: { type: [String, Number], required: true },
    endpoint: { type: String, required: true }
  },
  emits: ["deleted"],
  methods: {
    async handleDelete() {
      const confirmed = confirm("Bist du sicher, dass du dieses Element löschen möchtest?");
      if (!confirmed) return;
      try {
        await axios.delete(`${import.meta.env.VITE_API_URL}${this.endpoint}/${this.id}`);
        this.$emit("deleted", this.id);
      } catch (error) {
        console.error("Fehler beim Löschen:", error);
        alert("Löschen fehlgeschlagen.");
      }
    }
  }
};
</script>

<style scoped>
.delete-btn {
  background-color: #ff4d4d;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-weight: bold;
}
.delete-btn:hover {
  background-color: #e60000;
}
</style>
```

---

## PreviousTournaments  
**Datei:** `/views/PreviousTournaments.vue`  
**Zweck:** Anzeige und Verwaltung (Anzeigen, Laden, Löschen einzelner oder mehrerer Turniere)

### Erweiterung inkl. Selektion & Löschlogik

- **Komponenten-Import:**

```js
import LoescheButton from "@/components/LoescheButton.vue";
```

- **Template ergänzt:**  
  - Löschmodus aktivieren  
  - Auswahl einzelner Turniere  
  - Buttons: Löschen, Abbrechen, Alle löschen

- **Methoden für Auswahl & Löschung:**

```js
enableSelectMode() { ... }
cancelSelection() { ... }
confirmDeleteSelected() { ... }
confirmDeleteAll() { ... }

async deleteTournaments(ids) { ... }
```

- **Axios-Abfragen im Backend:**

```http
DELETE /tournaments/{id}
DELETE /tournaments/delete_plan/{id}
```

## ExportButton  
**Datei:** `/views/ExportButton.vue`  
**Zweck:** Exportiert Turnier- und Spielplandaten als CSV

### Funktionalitäten:

- Öffnet ein Dialogfenster mit:
  - Auswahl von Turnieren  
  - Anzeige der Spielanzahl  
  - Export-Button

- **Methoden:**

```js
async openExportDialog() { ... }
async fetchTournaments() { ... }
async onTournamentSelect() { ... }
async exportToCSV() { ... }
```

- **CSV-Struktur:**

```
Spiel ID;Gruppe;Team A;Team B;Ergebnis;Schiedsrichter;Feld;Startzeit
```

---


## TurnierErstellungsschritte <a name="turnier-erstellungsschritte"></a>

### Schritt 1 (`/views/TournamentStep1.vue`)
| Funktion | Validierungsregeln |
|----------|--------------------|
| Grundlegende Turnierkonfiguration | - Turniername erforderlich<br>- Positive numerische Werte<br>- Gültige Zeitformate |

### Schritt 2 (`/views/TournamentStep2.vue`)
| Funktion | Validierungsregeln |
|----------|--------------------|
| Detaillierte Gruppen- und Pausenkonfiguration | - Gruppennamen erforderlich<br>- Mind. 2 Teams/Gruppe<br>- Gültige Pausendauern |

## API-Dokumentation <a name="api-dokumentation"></a>

### Endpunkte

| Endpunkt               | Methode | Beschreibung                   | Parameter         |
|------------------------|---------|--------------------------------|-------------------|
| `/tournaments/`        | GET     | Liste aller Turniere           | Keine            |
| `/tournaments/:id`     | GET     | Turnierdetails abrufen         | `id`             |
| `/tournament/`         | POST    | Neues Turnier erstellen        | Turnier-Objekt   |
| `/match/:gameID`       | PUT     | Spielergebnis aktualisieren    | Ergebnis-Objekt  |

### Anfrage-/Antwort-Beispiele

**Turnier erstellen (POST /tournament/)**

```javascript
// Anfrage
{
  "name": "Winterturnier",
  "num_fields": 2,
  "return_match": true,
  "number_of_stages": 2,
  "start": "09:00",
  "period": 15,
  "warm_up": 5,
  "num_breaks": 1,
  "break_length": [10],
  "break_times": ["12:00"],
  "stage_name": ["Gruppe A", "Gruppe B"],
  "num_teams": [4, 4]
}

// Antwort
{
  "status": "erfolg",
  "tournament_id": 123
}
```

## Styleguide <a name="styleguide"></a>

### Design-System

#### Farbpalette
- **Primär:** `#004d40` (Dunkles Petrol)
- **Sekundär:** `#00796b` (Mittleres Petrol)
- **Akzent:** `#26a69a` (Helles Petrol)

#### Typografie
- **Hauptschrift:** Segoe UI
- **Fallback:** Arial, sans-serif
- **Grundgröße:** 16px
#
### Wiederverwendbare Komponenten

#### HomeButton
**Eigenschaften:**
| Name      | Typ     | Werte | Beschreibung|
|-----------|---------|----------------------------|-------------|
| `color`   | String  | `primary`, `secondary`     | Bestimmt die Button-Farbe  |
| `size`    | String  | `small`, `medium`, `large` | Bestimmt die Button-Größe  |
| `disabled`| Boolean | `true`, `false`            | Deaktiviert den Button     |
#
**Ereignisse:**
| Name     | Beschreibung                          |
|----------|---------------------------------------|
| `click`  | Wird bei Button-Klick ausgelöst       |
#
#### FormField
**Eigenschaften:**
| Name         | Typ     | Beschreibung                          |
|--------------|---------|---------------------------------------|
| `label`      | String  | Beschriftung des Eingabefelds         |
| `type`       | String  | `text`, `number`, `time` (Eingabetyp) |
| `modelValue` | Variabel| Gebundener Wert des Eingabefelds      |
#

## Entwicklungsanleitung <a name="entwicklungsanleitung"></a>

### Setup
```bash
# Abhängigkeiten installieren
npm install

# Entwicklungsserver starten
npm run dev
```
```
# Produktions-Build erstellen
npm run build

# Code-Linting und automatische Fehlerbehebung
npm run lint
```

```
# Unit-Tests ausführen
npm run test:unit

# End-to-End-Tests ausführen
npm run test:e2e
```


