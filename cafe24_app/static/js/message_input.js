Vue.component('message-input', {
    template: '#messageInput',
    data: function() {
        return {
            input_message: '',
            max_height: 73
        }
    },
    methods: {
        inputHandler: function(e) {
            if (e.keyCode === 13 && !e.shiftKey) {
                e.preventDefault();
                this.input();
            }
            this.resize(e);
        },
        input() {
            // '\n'만 있을 경우에도 입력 안되게 해야함. 비속어 걸러주는 것도 있으면 좋을 것 같음.
            // 조건을 만족할 때만 입력 버튼이 생기면 더 멋질 것 같다.
            if (this.input_message) {
                this.$emit('inputmessage', this.input_message);
                this.input_message = '';
            }
        },
        resize: function(e) {
            var textarea = e.target;
            if ((2 + textarea.scrollHeight) <= this.max_height) {
                textarea.style.overflowY = 'hidden';
                textarea.style.height = '0';
                textarea.style.height = (2 + textarea.scrollHeight) + 'px';
            } else {
                textarea.style.overflowY = 'visible';
                textarea.scrollTop = textarea.scrollHeight;
            }
        }
    }
})