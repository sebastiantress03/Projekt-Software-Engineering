<template>
    <label class="form-field">
        <span class="form-label">{{ label }}</span>
        <slot />
    </label>
</template>

<script>
export default {
    name: "FormField",
    props: {
        label: { type: String, required: true },
    },
};
</script>

<style scoped>
.form-field {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    font-weight: bold;
    font-size: 15px;
    color: #004d40;
}
.form-label {
    min-width: 160px;
}
</style>
