<template>
    <div class="match-card" @click="handleClick">
        <div class="match-header">
            <span class="group" :class="match.groupColor">{{
                match.group
            }}</span>
            <span class="field">Feld {{ match.field }}</span>
            <span class="time">{{ match.startTime }}</span>
        </div>
        <div class="match-info">
            <strong>{{ match.match }}</strong>
            <span
                v-if="match.scoreA !== null && match.scoreB !== null"
                class="score"
            >
                {{ match.scoreA }} : {{ match.scoreB }}
            </span>
            <span v-else class="score-placeholder">Ergebnis eintragen</span>
        </div>
        <div class="ref">Schiri: {{ match.ref }}</div>
    </div>
</template>

<script>
/**
 * @component MatchCard
 * @description
 * Zeigt die Informationen eines einzelnen Spiels (Match) an, inklusive Teams, Gruppe, Feld, Uhrzeit, Schiedsrichter und Ergebnis.
 *
 * @props
 * @prop {Object} match - Das Match-Objekt mit Feldern wie teamA, teamB, group, field, startTime, ref, scoreA, scoreB, groupColor, match (String für Anzeige).
 *
 * @emits open-popup - Wird ausgelöst, wenn auf die MatchCard geklickt wird, und gibt das Match-Objekt zurück.
 *
 * @example
 * <MatchCard :match="matchObj" @open-popup="handlePopup" />
 */
export default {
    name: "MatchCard",
    props: {
        match: {
            type: Object,
            required: true,
        },
    },
    methods: {
        handleClick() {
            this.$emit("open-popup", this.match);
        },
    },
};
</script>

<style scoped>
/* Basis-Styling für die Match-Karte */
.match-card {
    background: #f9f9f9;
    border-radius: 10px;
    margin: 10px 0;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(27, 66, 62, 0.08);
    cursor: pointer;
    transition: box-shadow 0.2s;
    border-left: 6px solid #387d75;
}

/* Hover-Effekt */
.match-card:hover {
    box-shadow: 0 4px 16px rgba(27, 66, 62, 0.18);
    background: #e6f2ef;
}

/* Header-Bereich (Gruppe, Feld, Zeit) */
.match-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    font-size: 14px;
}

/* Gruppen-Badge */
.group {
    font-weight: bold;
    padding: 2px 8px;
    border-radius: 6px;
    background: #387d75;
    color: #fff;
}

/* Gruppenvarianten */
.group.fun {
    background: #fbc02d;
    color: #222;
}
.group.schwitzer {
    background: #e57373;
    color: #fff;
}

/* Feld und Zeit */
.field {
    color: #1b423e;
    font-size: 13px;
}
.time {
    color: #387d75;
    font-size: 13px;
}
.match-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    margin-bottom: 4px;
}
.score {
    font-weight: bold;
    color: #387d75;
    margin-left: 10px;
}
.score-placeholder {
    color: #bbb;
    font-style: italic;
    margin-left: 10px;
}
.ref {
    font-size: 12px;
    color: #888;
    margin-top: 2px;
}
</style>
