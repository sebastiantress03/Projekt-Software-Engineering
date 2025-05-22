<template>
  <div class="create">
    <h2>Gruppen & Pausen</h2>

    <div v-for="(group, index) in stages" :key="index" class="group-block">
      <label>
        Gruppenname:
        <input v-model="group.name" />
      </label>

      <label>
        Anzahl Teams:
        <input type="number" v-model.number="group.teams" min="1" />
      </label>
    </div>

    <button @click="addStage">+ Gruppe hinzufügen</button>

    <div class="break-section">
      <h3>Pausenzeiten (optional)</h3>
      <div v-for="(breakTime, i) in break_times" :key="i">
        <input type="time" v-model="break_times[i]" />
        <input type="number" placeholder="Länge (Minuten)" v-model.number="break_lenght[i]" />
      </div>
      <button @click="addBreak">+ Pause hinzufügen</button>
    </div>

    <div class="buttons">
      <button @click="goBack">Zurück</button>
      <button @click="submit">Daten übergeben</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Werte aus Step1
      step1Data: this.$route.query,

      // Gruppen
      stages: [
        { name: '', teams: 1 }
      ],

      // Pausen
      break_times: [],
      break_lenght: []
    }
  },
  methods: {
    addStage() {
      this.stages.push({ name: '', teams: 1 });
    },
    addBreak() {
      this.break_times.push('');
      this.break_lenght.push(5);
    },
    goBack() {
      this.$router.push('/step1');
    },
    submit() {
      const payload = {
        ...this.step1Data,
        stage_name: this.stages.map(g => g.name),
        number_of_teams: this.stages.map(g => g.teams),
        break_times: this.break_times,
        break_lenght: this.break_lenght
      };

      console.log('✅ Gesammelt & bereit für API:', payload);

      // hier könnte später fetch() an das Backend folgen
      this.$router.push('/');
    }
  }
}
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
.group-block, .break-section {
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
button {
  margin-top: 20px;
  padding: 12px 24px;
  border: none;
  background: #58aaa0;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
}
button:hover {
  background: #387d75;
}
.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}
</style>
