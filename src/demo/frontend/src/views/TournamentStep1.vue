<template>
  <form @submit.prevent="emitAndNext">
    <h2>Turnierdaten</h2>

    <label>
      Turnierbezeichnung:
      <input v-model="local.name" type="text" required />
    </label>

    <label>
      Anzahl der Felder:
      <input v-model.number="local.fields" type="number" min="1" />
    </label>

    <label>
      Pausenlänge (Minuten):
      <input v-model.number="local.breakLength" type="number" min="0" />
    </label>

    <label>
      Spielzeit (Minuten):
      <input v-model.number="local.matchTime" type="number" min="1" />
    </label>

    <label>
      Startzeit:
      <input v-model="local.startTime" type="time" />
    </label>

    <label>
      Spielplan-Typ:
      <select v-model="local.mode">
        <option value="hinrunde">Hinrunde</option>
        <option value="hinrueck">Hin- und Rückrunde</option>
      </select>
    </label>

    <button type="submit">Weiter zu Gruppen</button>
  </form>
</template>

<script>
export default {
  props: ['name', 'fields', 'breakLength', 'matchTime', 'startTime', 'mode'],
  data() {
    return {
      local: {
        name: this.name,
        fields: this.fields,
        breakLength: this.breakLength,
        matchTime: this.matchTime,
        startTime: this.startTime,
        mode: this.mode
      }
    }
  },
  methods: {
    emitAndNext() {
      this.$emit('update', { ...this.local })
      this.$emit('next')
    }
  }
}
</script>

<style scoped>
form {
  max-width: 600px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
input,
select {
  padding: 8px;
  font-size: 16px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  align-self: flex-end;
}
</style>
