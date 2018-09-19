Vue.component('user-chat', {
    template: '#userChat',
    data() {
        return {
            chats: this.messages
        }
    },
    props: {
        messages: { type: Array, required: true }
    }
})