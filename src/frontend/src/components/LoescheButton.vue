<template>
<button class="delete-btn" @click="handleDelete">
    Löschen
</button>

</template>

<script>
import axios from "axios";

export default {
    name: "LoescheButton",
props: {
    id: {
        type: [String, Number],
        required: true,
    },
    endpoint: {
        type: String,
        required: true,
      // Beispiel: "/tournaments" → ergibt DELETE /tournaments/{id}
    },
},
    emits: ["deleted"],
    methods: {
    async handleDelete() {
        const confirmed = confirm("Bist du sicher, dass du dieses Element löschen möchtest?");
        if (!confirmed) return;

        try {
        await axios.delete(`${import.meta.env.VITE_API_URL}${this.endpoint}/${this.id}`);
        this.$emit("deleted", this.id);
    } catch (error) {
        console.error("Fehler beim Löschen:", error);
        alert("Löschen fehlgeschlagen.");
        }
    },
},
};
</script>

<style scoped>
.delete-btn {
    background-color: #ff4d4d;
    border: none;
    padding: 10px 15px;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s ease;
}

.delete-btn:hover {
    background-color: #e60000;
}
</style>
