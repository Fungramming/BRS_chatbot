Vue.component('user-chat', {
    template: '#userChat',
    data() {
        return {
            chats: this.messages,
            minute_time: this.minute
        }
    },
    computed: {
        minute_time_str: function() {
            return this.minute_time.toLocaleTimeString().split(':').slice(0, 2).join(':');
        }
    },
    props: {
        messages: { type: Array, required: true },
        minute: { type: Object, required: true }
    }
})