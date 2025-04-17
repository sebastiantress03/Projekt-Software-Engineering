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
      this.$router.push({ name: 'TournamentStep2', query: this.form })
    }
  }
}
</script>

<style scoped>
.form-wrapper {
  max-width: 600px;
  margin: 40px auto;
  padding: 30px;
  border-radius: 10px;
  background-color: #1b423e;
  color: white;
  font-family: 'Segoe UI', sans-serif;
}

h2 {
  color: #cee9e6;
  margin-bottom: 25px;
  text-align: center;
}

label {
  display: block;
  margin-bottom: 15px;
  font-weight: 500;
}

input,
select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  margin-top: 5px;
  color: #222;
  box-sizing: border-box;
}

.buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

button {
  padding: 10px 20px;
  background-color: #58aaa0;
  color: #cee9e6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #387d75;
}
</style>
