new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data:{
        images: null,
    },
    created() {
        axios
            .get("/get_images/?images=0")
            .then(response => {
                new_images = response.data.images;
                this.images = new_images;
            })
    },
    computed: {
        images_now(){
            return this.images;
        },
    },
    mounted() {
        this.scroll()
    },
    methods: {
        scroll() {
            window.onscroll = () => {
                let length_to_bottom = document.documentElement.scrollTop + window.innerHeight >= document.documentElement.offsetHeight - 250;
                if (length_to_bottom) {
                    this.get_images();
                }
            }
        },
        delete_image(id) {
            axios
                .get("/?id=" + id)
                .then (response => {
                    let index = -1;
                    for (let i = 0;  i < this.images.length; i++) {
                        if (this.images[i]["id"] == id) {
                            index = i;
                        }
                    }
                    if (index == -1) {
                        alert("Ошибка удаления картинки");
                    }
                    else {
                        img = this.images[index];
                        this.images.splice(index, 1);
                    }
                })
            
        },
        get_images() {
            axios
            .get("/get_images/?images=" + this.images.length)
            .then(response => {
                new_images = response.data.images;
                for (let i = 0; i < new_images.length; i++) {
                    if (new_images[i]["id"] > this.images.length){
                        this.images.push(new_images[i])
                    }
                }
            })
        },
    }
});