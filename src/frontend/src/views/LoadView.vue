<template>
  <div class="load">
    <h2>Turnier laden</h2>
    <ul class="tournament-list">
      <li v-for="t in tournaments" :key="t.id" @click="viewPlan(t.id)">
        🏆 {{ t.name }} – {{ t.date }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'LoadView',
  data() {
    return {
      // Fiktive Turniere – später von der API ersetzt
      tournaments: [
        { id: 1, name: 'HTW Sommer Cup', date: '2024-07-20' },
        { id: 2, name: 'Winter Masters', date: '2024-12-10' }
      ]
    }
  },
  methods: {
    viewPlan(id) {
      // Wechselt zur Turnierplan-Ansicht mit ID
      this.$router.push({ name: 'TournamentPlan', params: { id } })
    }
  }
}
</script>

<style scoped>
.load {
  max-width: 700px;
  margin: 40px auto;
  font-family: 'Segoe UI', sans-serif;
}

.tournament-list {
  list-style: none;
  padding: 0;
}

.tournament-list li {
  background: #eee;
  margin-bottom: 10px;
  padding: 15px 20px;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.tournament-list li:hover {
  background: #ddd;
}
</style>
