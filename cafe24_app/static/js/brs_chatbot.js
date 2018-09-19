Vue.config.devtools = true

var app = new Vue({
    el: '#brs',
    data: {
        chatbot: false,
        brs_style: 'width: 76px !important; height: 76px !important; bottom: 24px; right: 24px;',
        conversation: [{
                bot: true,
                minute_time: new Date(new Date().setSeconds(0)),
                chats: [
                    { time: new Date(), message: "Alright great. Let's get you setup with a demo of BRS Chatbot." },
                    { time: new Date(), message: "What are you interested in using BRS Chatbot for?" }
                ]
            },
            {
                bot: false,
                minute_time: new Date(new Date().setSeconds(0)),
                chats: [
                    { time: new Date(), message: "Support" }
                ]
            },
            {
                bot: true,
                minute_time: new Date(new Date().setSeconds(0)),
                chats: [
                    { time: new Date(), message: "OK got it." },
                    { time: new Date(), message: "What kinds of support features are you looking for?" }
                ]
            },
            {
                bot: false,
                minute_time: new Date(new Date().setSeconds(0)),
                chats: [
                    { time: new Date(), message: "BRS Chatbot hosted help docs BRS Chatbot hosted help docs" }
                ]
            }
        ]
    },
    methods: {
        show: function() {
            this.chatbot = true;
            this.brs_style = 'width: 400px !important; height: 80% !important; bottom: 0; right: 0;'
        },
        hide: function() {
            this.chatbot = false;
            this.brs_style = 'width: 76px !important; height: 76px !important; bottom: 24px; right: 24px;'
        },
        inputEvent: function(msg) {
            var now = new Date();
            var last_speaker = this.conversation[this.conversation.length - 1];

            var time_criteria = new Date(last_speaker.minute_time.valueOf());
            var new_minute = time_criteria.getMinutes() + 1;
            time_criteria.setMinutes(new_minute);

            var chat = { time: new Date(now.valueOf()), message: msg };
            if (last_speaker.bot || (now > time_criteria)) {
                var new_speaker = { bot: false, minute_time: new Date(now.setSeconds(0)), chats: [] };
                new_speaker.chats.push(chat);
                this.conversation.push(new_speaker);
            } else {
                last_speaker.chats.push(chat);
            }

            // var chat = { time: '', message: msg };
            // this.conversation[this.conversation.length - 1].chats.push(chat);
        }
    }
})