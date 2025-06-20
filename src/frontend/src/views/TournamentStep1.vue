<template>
    <div class="form-wrapper">
        <h2>Turnier erstellen</h2>

        <div class="form-section">
            <FormField label="Turniername:">
                <input v-model="form.name" type="text" />
            </FormField>

            <FormField label="Anzahl der Felder:">
                <input v-model.number="form.num_fields" type="number" min="1" />
            </FormField>

            <FormField label="Hin- & Rückrunde:">
                <select v-model="form.return_match">
                    <option value="true">Ja</option>
                    <option value="false">Nein</option>
                </select>
            </FormField>

            <FormField label="Anzahl Gruppen:">
                <input
                    v-model.number="form.number_of_stages"
                    type="number"
                    min="1"
                />
            </FormField>

            <FormField label="Startzeit:">
                <input v-model="form.start" type="time" step="1800" />
            </FormField>

            <FormField label="Spielzeit (Min):">
                <input
                    v-model.number="form.period"
                    type="number"
                    min="1"
                    step="5"
                />
            </FormField>

            <FormField label="Aufwärmzeit (Min):">
                <input
                    v-model.number="form.warm_up"
                    type="number"
                    min="0"
                    step="5"
                />
            </FormField>

            <FormField label="Anzahl Pausen:">
                <input v-model.number="form.num_breaks" type="number" min="0" />
            </FormField>
        </div>

        <div class="buttons">
            
            <ZuruckButton
            color="secondary"
                size="large"
                @click="goBack"
                position
                
            >
            Zurück
            </ZuruckButton>

            <HomeButton
                color="secondary"
                size="large"
                :disabled="form.name === ''"
                @click="goToNext"
            >
                Weiter zu Gruppen
            </HomeButton>


        </div>
    </div>
</template>

<script>
import HomeButton from "../components/HomeButton.vue";
import FormField from "../components/FormField.vue";
import ZuruckButton from "@/components/ZuruckButton.vue";

export default {
    name: "TournamentStep1",
    components: { HomeButton, FormField, ZuruckButton},
    data() {
        return {
            form: {
                name: "",
                num_fields: 1,
                return_match: "true",
                number_of_stages: 1,
                start: "09:00",
                period: 10,
                warm_up: 5,
                num_breaks: 1,
            },
        };
    },
    methods: {
        goToNext() {
            if (!this.form.name.trim()) {
                alert("Bitte geben Sie einen Turniernamen ein!");
                return;
            }
            this.$router.push({ name: "TournamentStep2", query: this.form });
        },
    },
};
</script>

<style scoped>
.form-wrapper {
    position: relative;
    max-width: 800px;
    margin: 40px auto;
    padding: 40px 50px;
    border: 2px solid #004d40;
    border-radius: 8px;
    background-color: #f9fdfc;
    font-family: Arial, sans-serif;
    color: #004d40;
}

h2 {
    font-size: 26px;
    margin-bottom: 30px;
    color: #004d40;
    border-bottom: 2px solid #004d40;
    padding-bottom: 10px;
    text-align: left;
}

label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    font-weight: bold;
    font-size: 15px;
    color: #004d40;
}

label input,
label select {
    flex: 1;
    margin-left: 20px;
    padding: 10px 12px;
    font-size: 15px;
    border-radius: 4px;
    border: 1px solid #bbb;
    background-color: #ffffff;
    color: #003333;
    box-sizing: border-box;
}

input[type="time"],
input[type="number"],
input[type="text"],
select {
    width: 100%;
}

.buttons {

    display: flex;
    justify-content: space-between; /* statt flex-end */
    margin-top: 40px;


}

.button-container {
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    margin-top: 40px;
}


button {
    padding: 12px 24px;
    background-color: #00796b;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #004d40;
}

.action-button {
    flex: 1;
    text-align: center;
    padding: 12px 24px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
    transition: background-color 0.3s;
}

</style>