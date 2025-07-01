# Tournament Management System - Comprehensive Documentation

## Inhaltsverzeichnis
1. [Systemübersicht](#system-uebersicht)
2. [Komponentendokumentation](#komponentendokumentation)
   - [TurnierErstellen](#turnier-erstellen)
   - [TurnierAuswertung](#turnier-auswertung)
   - [TurnierPlan](#turnier-plan)
   - [VorherigeTurniere](#vorherige-turniere)
   - [LoescheButton](#loeschebutton)
   - [PreviousTournaments (Erweitert)](#previoustournaments-erweitert)
   - [ExportButton](#exportbutton)
   - [TurnierErstellungsschritte](#turnier-erstellungsschritte)
3. [API-Dokumentation](#api-dokumentation)
4. [Styleguide](#styleguide)
5. [Entwicklungsanleitung](#entwicklungsanleitung)


## 1. Systemübersicht <a name="system-uebersicht"></a>

Das Turnierverwaltungssystem ist eine umfassende Anwendung, die speziell für die effiziente Organisation und Durchführung von Sportturnieren konzipiert wurde. Es bietet eine intuitive Benutzeroberfläche, die auf dem modernen JavaScript-Framework Vue.js basiert, und interagiert mit einem robusten Backend, um alle Aspekte der Turnierverwaltung abzudecken. Die Kernfunktionen des Systems umfassen:

*   **Turniererstellung und -konfiguration**: Ermöglicht Benutzern die Definition detaillierter Turnierparameter, einschließlich Turniername, Anzahl der Spielfelder, Rückspiele, Startzeiten, Spiel- und Aufwärmzeiten sowie Pausenkonfigurationen. Dies gewährleistet eine flexible Anpassung an verschiedene Turnierformate.
*   **Spielplanung**: Automatisiert die Erstellung von Spielplänen basierend auf den eingegebenen Turnierdaten. Der Spielplan berücksichtigt die Anzahl der Teams pro Gruppe und die Verfügbarkeit der Spielfelder, um eine faire und effiziente Spielabfolge zu gewährleisten.
*   **Ergebnisverfolgung und -auswertung**: Bietet Funktionen zur Echtzeit-Erfassung von Spielergebnissen und zur automatischen Berechnung von Tabellenständen. Die Auswertung umfasst detaillierte Statistiken wie Siege, Niederlagen, Punkte, Gegentore und Tordifferenzen, die eine transparente Leistungsübersicht ermöglichen.
*   **Teammanagement**: Unterstützt die Verwaltung von Teams innerhalb der Gruppen, einschließlich der Zuweisung von Teamnamen und der Festlegung der Teamanzahl pro Gruppe. Dies erleichtert die Strukturierung des Turniers und die Organisation der Teilnehmer.
*   **Historische Turnierdaten**: Ermöglicht den Zugriff auf und die Anzeige von zuvor gespeicherten Turnieren, was eine Nachverfolgung und Analyse vergangener Veranstaltungen ermöglicht. Benutzer können frühere Turnierpläne einsehen und bei Bedarf exportieren.

Das System ist modular aufgebaut, wobei das Frontend für die Benutzerinteraktion und das Backend für die Datenverarbeitung und -speicherung zuständig ist. Diese Trennung sorgt für Skalierbarkeit und Wartbarkeit der Anwendung.




## 2. Komponentendokumentation <a name="komponentendokumentation"></a>

Dieser Abschnitt beschreibt die zentralen Vue.js-Komponenten, aus denen die Benutzeroberfläche des Turnierverwaltungssystems aufgebaut ist. Jede Komponente ist so konzipiert, dass sie eine spezifische Funktionalität kapselt, was die Wiederverwendbarkeit und Wartbarkeit des Codes verbessert.

### 2.1. TurnierErstellen <a name="turnier-erstellen"></a>

Die Komponente `TurnierErstellen` stellt die zentrale Benutzeroberfläche zur Erfassung aller notwendigen Parameter für die Erstellung eines neuen Turniers dar. Sie ist als formularbasierte Ansicht implementiert, die eine intuitive und geführte Dateneingabe ermöglicht.

#### Datenstruktur

Die Komponente verwaltet die folgenden Datenfelder, die für die Konfiguration eines Turniers erforderlich sind:

```javascript
{
  tournament_name: "",       // (String) Name des Turniers (Pflichtfeld)
  number_of_fields: 1,       // (Number) Anzahl der verfügbaren Spielfelder (Minimum: 1)
  return_match: "true",      // (String) Gibt an, ob Rückspiele stattfinden sollen ("true" oder "false")
  time_to_start: "09:00",    // (String) Startzeit des Turniers im Format HH:mm
  game_time: 10,             // (Number) Dauer eines Spiels in Minuten
  warm_up_time: 5,           // (Number) Aufwärmzeit vor jedem Spiel in Minuten
  number_of_breaks: 1,       // (Number) Anzahl der geplanten Pausen
  break_length: [5],         // (Array<Number>) Dauer jeder Pause in Minuten
  break_times: [""],         // (Array<String>) Startzeiten der Pausen im Format HH:mm
  stage_name: ["Gruppe A"],  // (Array<String>) Namen der einzelnen Gruppen oder Phasen
  number_of_teams: [4]       // (Array<Number>) Anzahl der Teams in jeder Gruppe
}
```

#### Methoden

| Methode        | Parameter | Beschreibung                                                                                                |
| :------------- | :-------- | :---------------------------------------------------------------------------------------------------------- |
| `updateStages` | Keine     | Aktualisiert dynamisch die Liste der Gruppenfelder basierend auf der angegebenen Anzahl der Gruppen.          |
| `updateBreaks` | Keine     | Aktualisiert dynamisch die Liste der Pausenfelder basierend auf der angegebenen Anzahl der Pausen.            |
| `submit`       | Keine     | Führt eine Validierung der Formulardaten durch und sendet die Konfiguration an das Backend zur Verarbeitung. |

### 2.2. TurnierAuswertung <a name="turnier-auswertung"></a>

Diese Komponente ist für die Visualisierung der Turnierergebnisse und die Ermittlung der Gewinner zuständig. Sie bietet eine übersichtliche Darstellung der Tabellenstände und ermöglicht es den Benutzern, die Ergebnisse nach Gruppen zu filtern.

#### Dynamische Eigenschaften

| Eigenschaft     | Typ                | Beschreibung                                                                                             |
| :-------------- | :----------------- | :------------------------------------------------------------------------------------------------------- |
| `selectedGroup` | `String`           | Speichert die aktuell vom Benutzer ausgewählte Gruppe, um die angezeigten Ergebnisse zu filtern.         |
| `winners`       | `Computed<String[]>` | Eine berechnete Eigenschaft, die eine Liste der Gewinner für die aktuell ausgewählte Gruppe zurückgibt. |
| `results`       | `Computed<Object[]>` | Eine berechnete Eigenschaft, die die detaillierten Spielergebnisse für die ausgewählte Gruppe enthält.   |

#### Testdatenstruktur

Die Komponente erwartet eine Datenstruktur, die die Ergebnisse pro Gruppe organisiert:

```javascript
{
  "[gruppenName]": {
    "winners": ["Team Alpha", "Team Beta"],
    "results": [
      {
        "platz": 1,           // (Number) Endplatzierung des Teams
        "team": "Team Alpha", // (String) Name des Teams
        "s": 10,              // (Number) Anzahl der Siege
        "n": 1,               // (Number) Anzahl der Niederlagen
        "p": 130,             // (Number) Gesamtpunktzahl
        "g": 90,              // (Number) Anzahl der Gegentore
        "diff": 40            // (Number) Tordifferenz
      }
    ]
  }
}
```

### 2.3. TurnierPlan <a name="turnier-plan"></a>

Die Ansicht `TurnierPlan` ist das Herzstück der interaktiven Turnierverwaltung. Sie visualisiert den gesamten Spielplan und ermöglicht die Eingabe von Spielergebnissen in Echtzeit.

#### Hauptfunktionen

*   **Interaktive Spielkarten**: Jedes Spiel wird als eine Karte dargestellt, die wichtige Informationen wie die beteiligten Teams, die geplante Startzeit und das Spielfeld anzeigt.
*   **Ergebniseingabe**: Durch Klicken auf eine Spielkarte öffnet sich ein modales Fenster, in dem die Ergebnisse für das jeweilige Spiel eingegeben und gespeichert werden können.
*   **Team-Filterung**: Ein Dropdown-Menü ermöglicht die Filterung des Spielplans nach einem bestimmten Team, um dessen Spiele schnell zu finden.
*   **Visuelle Gruppierung**: Die Spiele sind visuell nach den Spielfeldern gruppiert, auf denen sie stattfinden, was eine klare und intuitive Übersicht schafft.

#### API-Integration

| Methode | Endpunkt                          | Beschreibung                                      |
| :------ | :-------------------------------- | :------------------------------------------------ |
| `GET`   | `/tournaments/:id`                | Lädt die detaillierten Daten eines Turniers.      |
| `PUT`   | `/tournaments/match_plan/match/:gameID` | Aktualisiert das Ergebnis eines bestimmten Spiels. |

### 2.4. VorherigeTurniere <a name="vorherige-turniere"></a>

Diese Komponente bietet eine Übersicht über alle in der Vergangenheit erstellten und gespeicherten Turniere. Sie dient als Archiv und ermöglicht den schnellen Zugriff auf historische Daten.

#### Datenfluss

1.  **Laden der Turnierliste**: Beim Laden der Komponente wird eine Anfrage an die API gesendet, um eine Liste aller gespeicherten Turniere abzurufen.
2.  **Anzeige als Buttons**: Jedes Turnier wird als ein klickbarer Button dargestellt, der den Namen des Turniers anzeigt.
3.  **Navigation zum Turnierplan**: Bei Auswahl eines Turniers wird der Benutzer zur `TurnierPlan`-Ansicht weitergeleitet, die den detaillierten Spielplan des ausgewählten Turniers anzeigt.

### 2.5. LoescheButton <a name="loeschebutton"></a>

Der `LoescheButton` ist eine generische und wiederverwendbare Komponente, die eine standardisierte Funktionalität zum Löschen von Elementen bereitstellt. Sie kann für das Löschen von Turnieren, Teams oder anderen Entitäten verwendet werden.

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
      const confirmed = confirm("Sind Sie sicher, dass Sie dieses Element löschen möchten?");
      if (!confirmed) return;
      try {
        await axios.delete(`${import.meta.env.VITE_API_URL}${this.endpoint}/${this.id}`);
        this.$emit("deleted", this.id);
      } catch (error) {
        console.error("Fehler beim Löschen:", error);
        alert("Das Löschen ist fehlgeschlagen.");
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

### 2.6. PreviousTournaments (Erweitert) <a name="previoustournaments-erweitert"></a>

Die erweiterte Version der `PreviousTournaments`-Ansicht integriert eine Auswahl- und Löschlogik, die es Benutzern ermöglicht, mehrere Turniere gleichzeitig zu verwalten.

#### Erweiterungen

*   **Komponenten-Import**: Importiert den `LoescheButton` für die Löschfunktionalität.
*   **Template-Anpassungen**: Das Template wurde um einen Löschmodus erweitert, der die Auswahl einzelner Turniere über Checkboxen ermöglicht. Zusätzliche Buttons für "Löschen", "Abbrechen" und "Alle löschen" wurden hinzugefügt.
*   **Methoden für Auswahl & Löschung**: Neue Methoden wie `enableSelectMode`, `cancelSelection`, `confirmDeleteSelected`, `confirmDeleteAll` und `deleteTournaments` wurden implementiert, um die Auswahl- und Löschlogik zu steuern.

#### API-Integration

| Methode | Endpunkt                        | Beschreibung                               |
| :------ | :------------------------------ | :----------------------------------------- |
| `DELETE`| `/tournaments/{id}`             | Löscht ein einzelnes, spezifisches Turnier. |
| `DELETE`| `/tournaments/delete_plan/{id}` | Löscht den Spielplan eines Turniers.       |

### 2.7. ExportButton <a name="exportbutton"></a>

Diese Komponente ermöglicht den Export von Turnier- und Spielplandaten in das CSV-Format, um eine externe Weiterverarbeitung und Analyse zu ermöglichen.

#### Funktionalitäten

*   **Export-Dialog**: Öffnet ein Dialogfenster, in dem Benutzer die zu exportierenden Turniere auswählen können. Der Dialog zeigt auch die Gesamtzahl der Spiele an, die exportiert werden.
*   **Methoden**: Beinhaltet Methoden wie `openExportDialog`, `fetchTournaments`, `onTournamentSelect` und `exportToCSV`, um den Exportprozess zu steuern.

#### CSV-Struktur

Die exportierte CSV-Datei hat die folgende Spaltenstruktur:

`Spiel ID;Gruppe;Team A;Team B;Ergebnis;Schiedsrichter;Feld;Startzeit`

### 2.8. TurnierErstellungsschritte <a name="turnier-erstellungsschritte"></a>

Der Prozess der Turniererstellung ist in zwei logische Schritte unterteilt, um die Benutzerfreundlichkeit zu verbessern und die Komplexität zu reduzieren.

#### Schritt 1 (`/views/TournamentStep1.vue`)

*   **Funktion**: Erfasst die grundlegenden Turnierkonfigurationen.
*   **Validierungsregeln**: Stellt sicher, dass der Turniername ausgefüllt ist, alle numerischen Werte positiv sind und die Zeitformate korrekt eingegeben werden.

#### Schritt 2 (`/views/TournamentStep2.vue`)

*   **Funktion**: Ermöglicht die detaillierte Konfiguration von Gruppen und Pausen.
*   **Validierungsregeln**: Stellt sicher, dass Gruppennamen vorhanden sind, jede Gruppe mindestens zwei Teams hat und die Pausendauern gültig sind.




## 3. API-Dokumentation <a name="api-dokumentation"></a>

Die API (Application Programming Interface) dient als Schnittstelle zwischen dem Frontend und dem Backend des Turnierverwaltungssystems. Sie ermöglicht den Datenaustausch und die Ausführung von serverseitigen Operationen. Die API ist nach den Prinzipien von REST (Representational State Transfer) gestaltet und verwendet das JSON-Format für den Datenaustausch.

### 3.1. Endpunkte

Die folgende Tabelle listet die verfügbaren API-Endpunkte, die unterstützten HTTP-Methoden und deren jeweilige Funktionen auf:

| Endpunkt                  | Methode | Beschreibung                                         | Parameter         |
| :------------------------ | :------ | :--------------------------------------------------- | :---------------- |
| `/tournaments/`           | `GET`   | Ruft eine Liste aller verfügbaren Turniere ab.         | Keine             |
| `/tournaments/:id`        | `GET`   | Ruft die detaillierten Informationen eines spezifischen Turniers ab. | `id` (Pfad)       |
| `/tournament/`            | `POST`  | Erstellt ein neues Turnier basierend auf den übergebenen Daten. | Turnier-Objekt (Body) |
| `/match/:gameID`          | `PUT`   | Aktualisiert das Ergebnis eines bestimmten Spiels.     | Ergebnis-Objekt (Body) |
| `/tournaments/:id`        | `DELETE`| Löscht ein spezifisches Turnier.                      | `id` (Pfad)       |
| `/tournaments/:id/export` | `GET`   | Exportiert die Daten eines Turniers im CSV-Format.   | `format=csv` (Query) |

### 3.2. Anfrage- und Antwortbeispiele

#### Turnier erstellen (`POST /tournament/`)

**Anfrage-Body:**

```json
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
```

**Antwort-Body (Erfolg):**

```json
{
  "status": "erfolg",
  "tournament_id": 123
}
```



## 4. Styleguide <a name="styleguide"></a>

Der Styleguide definiert die visuellen und gestalterischen Richtlinien für die Frontend-Entwicklung. Er stellt sicher, dass die Benutzeroberfläche ein konsistentes und ansprechendes Erscheinungsbild aufweist.

### 4.1. Design-System

#### Farbpalette

*   **Primärfarbe**: `#004d40` (Dunkles Petrol) - Wird für Hauptelemente wie Header und wichtige Buttons verwendet.
*   **Sekundärfarbe**: `#00796b` (Mittleres Petrol) - Wird für sekundäre Elemente und Hover-Effekte eingesetzt.
*   **Akzentfarbe**: `#26a69a` (Helles Petrol) - Dient zur Hervorhebung von aktiven Elementen und für Call-to-Action-Buttons.

#### Typografie

*   **Hauptschriftart**: `Segoe UI` - Die bevorzugte Schriftart für alle Textelemente.
*   **Fallback-Schriftart**: 
(Content truncated due to size limit. Use line ranges to read in chunks)