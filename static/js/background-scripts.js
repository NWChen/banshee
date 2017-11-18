$(document).ready(function() {

    const get_inputs = function getValuesOfAllInputs() {
        var inputs = {
            username: $('#username').val(),
            earliest_date: $('#earliest-date').val(),
            latest_date: $('#latest-date').val(),
            keywords: $('#keywords').val(),
            retweets: $('#retweets').val()
        };
        return inputs;
    };

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stream');
    socket.on('connect', function() {
        console.log('CONNECTED');
        $('#search').click(function() {
            inputs = get_inputs();
            console.log(inputs);
        });
    });
});
