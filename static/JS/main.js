new Vue({
    delimiters: ['[[', ']]'],
    methods: {
        delete_image(id) {
            axios
                .get("/?image=" + id)
            this.inputs.splice(id, 1)
        }
    }
});