Vue.component('message-input', {
    template: '#messageInput',
    data: function() {
        return {
            input_message: ''
        }
    },
    methods: {
        inputHandler: function(e) {
            if (e.keyCode === 13 && !e.shiftKey) {
                e.preventDefault();
                this.input();
            }
        },
        input() {
            if (this.input_message) {
                this.$emit('inputmessage', this.input_message);
                this.input_message = '';
            }
        }
    }
})