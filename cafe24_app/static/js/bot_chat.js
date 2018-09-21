Vue.component('bot-chat', {
    template: '#botChat',
    data() {
        return {
            chats: this.messages,
            minute_time: this.minute
        }
    },
    props: {
        messages: { type: Array, required: true },
        minute: { type: Object, required: true }
    }
})