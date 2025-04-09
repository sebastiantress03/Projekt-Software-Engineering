<template>
  <form @submit.prevent="$emit('submit')">
    <h2>Leistungsgruppen</h2>

    <div
      v-for="(group, index) in local.groups"
      :key="index"
      class="group-block"
    >
      <label>
        Gruppe {{ index + 1 }} – Bezeichnung:
        <input v-model="group.name" type="text" />
      </label>

      <label>
        Teamanzahl:
        <input v-model.number="group.teamCount" type="number" min="1" />
      </label>
    </div>

    <button type="button" @click="addGroup">+ Gruppe hinzufügen</button>

    <div class="buttons">
      <button type="button" @click="$emit('back')">Zurück</button>
      <button type="submit">Turnier erstellen</button>
    </div>
  </form>
</template>

<script>
export default {
  props: ['groups'],
  data() {
    return {
      local: {
        groups: this.groups
      }
    }
  },
  methods: {
    addGroup() {
      this.local.groups.push({ name: '', teamCount: 1 })
      this.$emit('update', { ...this.$props, groups: this.local.groups })
    }
  },
  watch: {
    local: {
      deep: true,
      handler(newVal) {
        this.$emit('update', { ...this.$props, ...newVal })
      }
    }
  }
}
</script>

<style scoped>
.group-block {
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
}
.buttons {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
</style>
