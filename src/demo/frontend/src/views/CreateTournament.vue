<template>
  <div class="create">
    <h2>Turnier erstellen</h2>

    <!-- BASISDATEN -->
    <label>Turniername:
      <input v-model="form.tournament_name" required/>
    </label>

    <label>Anzahl der Felder:
      <input type="number" v-model.number="form.number_of_fields" min="1" />
    </label>

    <label>Hin- & Rückrunde:
      <select v-model="form.return_match">
        <option value="true">Ja</option>
        <option value="false">Nein</option>
      </select>
    </label>

    <label>Anzahl Gruppen:
      <input type="number" v-model.number="form.number_of_stages" min="1" @change="updateStages" />
    </label>

    <label>Startzeit:
      <input type="time" v-model="form.time_to_start" />
    </label>

    <label>Spielzeit (Minuten):
      <input type="number" v-model.number="form.game_time" min="1" />
    </label>

    <label>Aufwärmzeit (Minuten):
      <input type="number" v-model.number="form.warm_up_time" min="0" />
    </label>

    <label>Anzahl Pausen:
      <input type="number" v-model.number="form.number_of_breaks" min="0" @change="updateBreaks" />
    </label>

    <!-- GRUPPEN -->
    <h3>Gruppen</h3>
    <div v-for="(name, index) in form.stage_name" :key="'group'+index">
      <label>Gruppenname:
        <input v-model="form.stage_name[index]" />
      </label>

      <label>Teamanzahl:
        <input type="number" v-model.number="form.number_of_teams[index]" min="1" />
      </label>
    </div>

    <!-- PAUSEN -->
    <h3>Pausenzeiten</h3>
    <div v-for="(pause, index) in form.break_length" :key="'pause'+index">
      <label>Dauer der Pause {{ index + 1 }} (Minuten):
        <input type="number" v-model.number="form.break_length[index]" min="1" />
      </label>

      <label>Beginn der Pause {{ index + 1 }}:
        <input type="time" v-model="form.break_times[index]" />
      </label>
    </div>

    <button @click="submit">✅ Testweise übergeben</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        tournament_name: '',
        number_of_fields: 1,
        return_match: 'true',
        number_of_stages: 1,
        time_to_start: '09:00',
        game_time: 10,
        warm_up_time: 5,
        number_of_breaks: 1,
        break_length: [5],
        stage_name: ['Gruppe A'],
        number_of_teams: [4],
        break_times: ['10:00']
      }
    }
  },
  methods: {
    updateStages() {
      this.form.stage_name = Array(this.form.number_of_stages).fill('').map((_, i) => `Gruppe ${String.fromCharCode(65 + i)}`)
      this.form.number_of_teams = Array(this.form.number_of_stages).fill(4)
    },
    updateBreaks() {
      this.form.break_length = Array(this.form.number_of_breaks).fill(5)
      this.form.break_times = Array(this.form.number_of_breaks).fill('10:00')
    },
    submit() {
        // Kleine Validierung für Name und Anz Felder
        if (!this.form.tournament_name) {
            alert('Turniername ist erforderlich!')
            return}
        if (this.form.number_of_fields < 1) {
            alert('Anzahl der Felder muss mindestens 1 sein!')
            return}
        console.log('Daten zur Übergabe (Frontend):', this.form)
        alert('✅ Daten wurden simuliert übergeben (Konsole prüfen)')
        // Später hier POST an API möglich
    }
  }
}
</script>

<style scoped>
.create {
  max-width: 700px;
  margin: 40px auto;
  background: #f8f8f8;
  padding: 30px;
  border-radius: 10px;
  font-family: sans-serif;
}

label {
  display: block;
  margin-bottom: 15px;
}

input, select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
button {
  margin-top: 20px;
  padding: 10px 20px;
  background: green;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
