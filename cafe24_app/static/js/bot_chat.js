Vue.component('bot-chat', {
    template: '#botChat',
    data() {
        return {
            chats: this.messages
        }
    },
    props: {
        messages: { type: Array, required: true }
    }
})