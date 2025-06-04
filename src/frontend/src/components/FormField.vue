<template>
    <label class="form-field">
        <span class="form-label">{{ label }}</span>
        <slot />
    </label>
</template>

<script>
/**
 * @component FormField
 * @description Eine Layout-Komponente zur Darstellung eines Formularfeldes mit Label und Inhalt über einen Slot.
 *
 * @props
 * @prop {String} label – Der Text, der als Label links vom Inhalt angezeigt wird.
 *
 * @slots
 * default – Der Inhalt (z. B. ein Eingabefeld), der rechts vom Label angezeigt wird.
 *
 * @example
 * <FormField label="Name">
 *   <input type="text" v-model="name" />
 * </FormField>
 */
export default {
    name: "FormField",
    props: {

        /**
         * Das Textlabel, das links neben dem Eingabefeld angezeigt wird.
         */
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
