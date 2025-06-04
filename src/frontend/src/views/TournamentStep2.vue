<template>
    <div class="create">
        <h2>Gruppen & Pausen</h2>

        <div v-for="(group, index) in stages" :key="index" class="group-block">
            <FormField :label="`Gruppenname:`">
                <input v-model="group.name" />
            </FormField>
            <FormField :label="`Anzahl Teams:`">
                <input type="number" v-model.number="group.teams" min="2" />
            </FormField>
        </div>

        <!-- <HomeButton @click="addStage">+ Gruppe hinzufügen</HomeButton> -->

        <div class="break-section">
            <h3>Pausenzeiten</h3>
            <div v-for="(breakTime, i) in num_breaks" :key="i">
                <FormField :label="`Beginn Pause ${i + 1}:`">
                    <input type="time" v-model="break_times[i]" />
                </FormField>
                <FormField :label="`Länge Pause ${i + 1} (Minuten):`">
                    <input
                        type="number"
                        placeholder="Länge (Minuten)"
                        v-model.number="break_length[i]"
                    />
                </FormField>
            </div>
            <!-- <HomeButton @click="addBreak">+ Pause hinzufügen</HomeButton> -->
        </div>

        <div class="buttons">
            <HomeButton color="secondary" @click="goBack">Zurück</HomeButton>
            <HomeButton color="primary" @click="submit" :disabled="isDisabled"
                >Daten übergeben</HomeButton
            >
        </div>
    </div>
</template>

<script>
import axios from "axios";
import FormField from "../components/FormField.vue";
import HomeButton from "../components/HomeButton.vue";

export default {
    components: { FormField, HomeButton },
    data() {
        return {
            step1Data: this.$route.query,
            break_times: [],
            break_length: [],
            stages: [],
            num_breaks: [],
        };
    },
    computed: {
        isDisabled() {
            // Gruppen: Name und Teams müssen ausgefüllt sein
            if (
                this.stages.some(
                    (g) => !g.name || !g.teams || isNaN(g.teams) || g.teams < 2
                )
            ) {
                return true;
            }
            // Pausen: Zeit und Länge müssen ausgefüllt und gültig sein
            if (
                this.num_breaks.length > 0 &&
                (this.break_times.length !== this.num_breaks.length ||
                    this.break_length.length !== this.num_breaks.length ||
                    this.break_times.some((t) => !t) ||
                    this.break_length.some((l) => !l || isNaN(l) || l <= 0))
            ) {
                return true;
            }
            return false;
        },
    },
    created() {
        // Parse number_of_stages from step1Data (may be string from query)
        const n = parseInt(this.step1Data.number_of_stages || 1, 10);
        this.stages = Array.from({ length: n }, () => ({ name: "", teams: 2 }));

        // Parse number_of_breaks from step1Data (may be string from query)
        const m = parseInt(this.step1Data.num_breaks || 0, 10);
        this.num_breaks = Array.from({ length: m }, () => "");
    },
    methods: {
        goBack() {
            this.$router.push("/step1");
        },
        submit() {
            const { number_of_stages, ...restStep1Data } = this.step1Data;
            const payload = {
                ...restStep1Data,
                break_length: [...this.break_length],
                break_times: [...this.break_times],
                stage_name: this.stages.map((g) => g.name),
                num_teams: this.stages.map((g) => g.teams),
            };
            console.log(
                "Payload an Backend:",
                JSON.stringify(payload, null, 2)
            );
            axios
                .post("http://localhost:8000/tournament/", payload)
                .then((response) => {
                    console.log("✅ API Antwort:", response.data);
                    this.$router.push("/");
                })
                .catch((error) => {
                    console.error("❌ Fehler bei der API:", error);
                    alert("Fehler beim Speichern des Turniers.");
                    this.$router.push("/");
                });
        },
    },
};
</script>

<style scoped>
.create {
    max-width: 700px;
    margin: 40px auto;
    padding: 30px;
    background: #1b423e;
    color: #f9f9f9;
    border-radius: 10px;
}
.group-block,
.break-section {
    background: #fff;
    padding: 15px;
    color: #222;
    margin-bottom: 15px;
    border-radius: 10px;
}
input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
}
.buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}
</style>
