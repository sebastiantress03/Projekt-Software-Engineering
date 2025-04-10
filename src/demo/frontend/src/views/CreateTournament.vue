<template>
  <div class="create">
    <h2>Turnier erstellen</h2>

    <!-- Schritt 1: Turnierdaten -->
    <div v-if="step === 1">
      <h3>Schritt 1: Turnierdaten</h3>

      <label>
        Turniername:
        <input v-model="form.name" />
      </label>

      <label>
        Anzahl der Felder:
        <input type="number" v-model.number="form.fields" min="1" />
      </label>

      <label>
        Pausenlänge (Minuten):
        <input type="number" v-model.number="form.breakLength" min="0" />
      </label>

      <label>
        Spielzeit (Minuten):
        <input type="number" v-model.number="form.matchTime" min="1" />
      </label>

      <label>
        Startzeit:
        <input type="time" v-model="form.startTime" />
      </label>

      <label>
        Spielplan-Typ:
        <select v-model="form.mode">
          <option value="hinrunde">Hinrunde</option>
          <option value="hinrueck">Hin- und Rückrunde</option>
        </select>
      </label>

      <button @click="step++">Weiter zu Gruppen</button>
    </div>

    <!-- Schritt 2: Gruppen -->
    <div v-else-if="step === 2">
      <h3>Schritt 2: Leistungsgruppen</h3>

      <div v-for="(group, i) in form.groups" :key="i" class="group-block">
        <label>
          Gruppe {{ i + 1 }} – Bezeichnung:
          <input v-model="group.name" placeholder="Gruppenname" />
        </label>

        <label>
          Teamanzahl:
          <input type="number" v-model.number="group.teamCount" min="1" />
        </label>
      </div>

      <button @click="addGroup">+ Gruppe hinzufügen</button>

      <div class="buttons">
        <button @click="step--">Zurück</button>
        <button @click="submit">Turnier erstellen</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      step: 1,
      form: {
        name: '',
        fields: 1,
        breakLength: 5,
        matchTime: 10,
        startTime: '09:00',
        mode: 'hinrunde',
        groups: [
          { name: '', teamCount: 1 }
        ]
      }
    }
  },
  methods: {
    addGroup() {
      this.form.groups.push({ name: '', teamCount: 1 })
    },
    submit() {
  fetch('http://localhost:3000/api/tournaments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: this.form.name,
      fields: this.form.fields,
      breakLength: this.form.breakLength,
      matchTime: this.form.matchTime,
      startTime: this.form.startTime,
      mode: this.form.mode
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log('Gespeichert ✅', data)
    alert(`Turnier "${this.form.name}" wurde gespeichert ✅`)
    this.$router.push('/')
  })
  .catch(err => {
    console.error('Fehler beim Speichern ❌', err)
    alert('Speichern fehlgeschlagen ❌\nDetails siehe Konsole')
  })
}

  }
}
</script>
<style scoped>
:root {
  --background-color: #1f2d2b; /* Dunkelgrün / Petrol */
  --surface-color: #263a38; /* etwas heller */
  --input-bg: #f4f4f4;
  --text-color: #f9f9f9;
  --primary-color: #2ecc71;
  --button-bg: #2ecc71;
  --button-text: white;
  --border-radius: 10px;
}

.create {
  max-width: 700px;
  margin: 40px auto;
  font-family: 'Segoe UI', sans-serif;
  background: var(--surface-color);
  padding: 30px;
  border-radius: var(--border-radius);
  color: var(--text-color);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

body {
  background-color: var(--background-color);
}

h2, h3 {
  color: var(--primary-color);
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
  border: none;
  border-radius: var(--border-radius);
  background-color: var(--input-bg);
  font-size: 15px;
  margin-top: 5px;
  box-sizing: border-box;
  color: #222;
}

button {
  background-color: var(--button-bg);
  color: var(--button-text);
  border: none;
  border-radius: var(--border-radius);
  padding: 12px 24px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

button:hover {
  background-color: #27ae60;
  transform: scale(1.03);
}

.group-block {
  background: #ffffff;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: var(--border-radius);
  margin-bottom: 15px;
  color: #222;
}

.buttons {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
