<template>
  <div class="form-wrapper">
    <h2>Turnier erstellen</h2>

    <div class="form-section">
      <label>
        Turniername:
        <input v-model="form.tournament_name" type="text" />
      </label>

      <label>
        Anzahl der Felder:
        <input v-model.number="form.number_of_fields" type="number" min="1" />
      </label>

      <label>
        Hin- & Rückrunde:
        <select v-model="form.return_match">
          <option value="Ja">Ja</option>
          <option value="Nein">Nein</option>
        </select>
      </label>

      <label>
        Anzahl Gruppen:
        <input v-model.number="form.number_of_stages" type="number" min="1" />
      </label>

      <label>
        Startzeit:
        <input v-model="form.time_to_start" type="time" />
      </label>

      <label>
        Spielzeit (Minuten):
        <input v-model.number="form.game_time" type="number" min="1" />
      </label>

      <label>
        Aufwärmzeit (Minuten):
        <input v-model.number="form.warm_up_time" type="number" min="0" />
      </label>

      <label>
        Anzahl Pausen:
        <input v-model.number="form.number_of_breaks" type="number" min="0" />
      </label>
    </div>

    <div class="buttons">
      <button @click="goToNext">Weiter zu Gruppen</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        tournament_name: '',
        number_of_fields: 1,
        return_match: 'Ja',
        number_of_stages: 1,
        time_to_start: '09:00',
        game_time: 10,
        warm_up_time: 5,
        number_of_breaks: 1
      }
    }
  },
  methods: {
    goToNext() {
      //nochmal Validierung, in CreateTournament.vue ectl überflüssig
      if (!this.form.tournament_name.trim()) {
      alert('Bitte geben Sie einen Turniernamen ein!')
      return}
      this.$router.push({ name: 'TournamentStep2', query: this.form })
    }
  }
}
</script>

<style scoped>
.form-wrapper {
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
  justify-content: flex-end;
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
</style>

