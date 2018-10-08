Vue.config.devtools = true

var app = new Vue({
    el: '#chat',
    data: {
        test0: 'xyz',
        test: 'abc'
    },
    render: function(createElement) {
        return createElement('div', this.test0)
    }
})