<script setup>
import {ref} from 'vue'

    const props = defineProps({
        spielID: {
            type: Number,
            required: true,
        },
        teamID1: {
            type: Number,
            required: true,
        },
        teamID2: {
            type: Number,
            required: true,
        },
        spielergebnis1: {
            type: Number,
            required: true
        },
        spielergebnis2: {
            type: Number,
            required: true
        },
        hinrückspiel: {
            type: String,
            required: true
        }

    });

    const spielergebnis1 = ref(props.spielergebnis1);
    const spielergebnis2 = ref(props.spielergebnis2);

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
    <div class="ergebnistabelle">
        <div class="teamname">
            <div>Team {{ teamID1 }}</div>
            <div >Team {{ teamID2 }}</div>
        </div>
        <div>
            <input @input="saveChangesLocal()" class="inputfield" type="number" min="0" max="25" v-model="spielergebnis1" />
            vs.
            <input @input="saveChangesLocal()" class="inputfield" type="number" min="0" max="25" v-model="spielergebnis2" />
        </div>
        <div>
            {{ hinrückspiel }}
        </div>
    </div>

</template>

<style scoped>
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

    .inputfield{
        display: flex;
        border: 1px solid rgba(0,0,0,0.2);
        border-radius: 8px;
        width: 50px;
        flex-direction: row;
        cursor: pointer;
    }
    .teamname {
        display: flex;
        flex-direction: column;
        gap: 18px;
    }

    .save_Change {
        display: flex;
        flex-direction: row;
		background-color: rgba(0,0,0,0.2);
        cursor: pointer;
	}
</style>