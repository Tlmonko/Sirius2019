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
    methods: {
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
                        this.images.splice(img, 1);
                    }
                })
            
        },
        get_images() {
            alert(1);
            axios
                .get("/get_images/?images=" + images.length)
                .then(response => {
                    images = response.data.images;
                    this.images += images;
                })
        },
    }
});