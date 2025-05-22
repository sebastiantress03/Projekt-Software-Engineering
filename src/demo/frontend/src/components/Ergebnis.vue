<script setup>
import {ref} from 'vue'
/**
 * Komponente zur Anzeige und Bearbeitung von Spielergebnissen
 * @component
 * @description Ermöglicht die Eingabe von Ergebnissen für zwei Teams und speichert diese im LocalStorage.
 */
    const props = defineProps({

     /**
     * Eindeutige ID des Spiels
     * @type {Number}
     * @required
     */

        spielID: {
            type: Number,
            required: true,
        },

        /**
     * ID des ersten Teams
     * @type {Number}
     * @required
     */

        teamID1: {
            type: Number,
            required: true,
        },

        /**
     * ID des zweiten Teams
     * @type {Number}
     * @required
     */
        teamID2: {
            type: Number,
            required: true,
        },

    /**
     * Aktuelles Ergebnis von Team 1
     * @type {Number}
     * @required
     */

        spielergebnis1: {
            type: Number,
            required: true
        },

         /**
     * Aktuelles Ergebnis von Team 2
     * @type {Number}
     * @required
     */

        spielergebnis2: {
            type: Number,
            required: true
        },

     /**
     * Kennzeichnung ob Hin- oder Rückrundenspiel
     * @type {String}
     * @required
     * @example "Hinrunde" oder "Rückrunde"
     */
        hinrückspiel: {
            type: String,
            required: true
        }

    });

    // Reaktive Referenzen für die Spielergebnisse
    const spielergebnis1 = ref(props.spielergebnis1);
    const spielergebnis2 = ref(props.spielergebnis2);

    /**
 * Speichert die geänderten Ergebnisse im LocalStorage
 * @method
 * @description Aktualisiert die Ergebnisse im LocalStorage und behält eine Kopie der Originalwerte
 */
    function saveChangesLocal(){
        let storage = JSON.parse(localStorage.getItem("ergebnisse"));
        let data = storage[props.spielID] ||
        {
            "actual" : [props.spielID,props.teamID1,props.teamID2,spielergebnis1.value,spielergebnis2.value,props.hinrückspiel],
            "copy" : [props.spielID,props.teamID1,props.teamID2,props.spielergebnis1,props.spielergebnis2,props.hinrückspiel]
        };

        data["actual"][3] = spielergebnis1.value;
        data["actual"][4] = spielergebnis2.value;

        storage[props.spielID] = data;

        localStorage.setItem("ergebnisse",JSON.stringify(storage));
    }

</script>

<template>
    <!-- Container für die Ergebnisanzeige -->
    <div class="ergebnistabelle">
         <!-- Teamnamen Anzeige -->
        <div class="teamname">
            <div>Team {{ teamID1 }}</div>
            <div >Team {{ teamID2 }}</div>
        </div>

         <!-- Eingabefelder für Ergebnisse -->
        <div>
            <input @input="saveChangesLocal()" class="inputfield" type="number" min="0" max="25" v-model="spielergebnis1" />
            vs.
            <input @input="saveChangesLocal()" class="inputfield" type="number" min="0" max="25" v-model="spielergebnis2" />
        </div>

         <!-- Anzeige ob Hin- oder Rückrundenspiel -->
        <div>
            {{ hinrückspiel }}
        </div>
    </div>

</template>

<style scoped>

/* 
 * Haupt-Container für die Ergebnis-Tabelle.
 * - Flex-Layout für horizontale Anordnung der Inhalte
 * - Leichte Hintergrundfarbe und Rahmen zur Abgrenzung
 * - Innenabstand und abgerundete Ecken für visuelle Harmonie
 */
    .ergebnistabelle{
        display: flex;
        flex-direction: row;
        gap: 8px;
        border: 1px solid rgba(0,0,0,0.2);
        padding: 8px;
        margin: 8px;
        border-radius: 8px;
        background-color: rgba(0,0,0,0.1);
        border-color: rgba(0,0,0,0.2);
    }
/*
 * Eingabefelder für die Spielergebnisse.
 * - Feste Breite (50px) für einheitliches Erscheinungsbild
 * - Subtiler Rahmen und abgerundete Ecken
 * - Zeiger-Cursor zur Benutzerinteraktion
 */
    .inputfield{
        display: flex;
        border: 1px solid rgba(0,0,0,0.2);
        border-radius: 8px;
        width: 50px;
        flex-direction: row;
        cursor: pointer;
    }

    /*
 * Container für die Teamnamen.
 * - Vertikale Anordnung (Spaltenlayout)
 * - Großer Abstand (18px) zwischen den Teamnamen für bessere Lesbarkeit
 */
    .teamname {
        display: flex;
        flex-direction: column;
        gap: 18px;
    }
    
/*
 * (Optional) Save-Button-Stil (aktuell nicht im Template verwendet).
 * - Hervorgehobener Hintergrund für Interaktions-Elemente
 * - Zeigt Pointer-Cursor beim Hovern
 */
    .save_Change {
        display: flex;
        flex-direction: row;
		background-color: rgba(0,0,0,0.2);
        cursor: pointer;
	}
</style>