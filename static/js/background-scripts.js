$(document).ready(function() {

    // these long function names are essentially documentation, and should never be called
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

    const send_inputs = function sendValuesOfAllInputsToServerSocket(socket, inputs) {
        socket.emit('inputs', inputs);
    };

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stream');
    socket.on('connect', function() {
        console.log('CONNECTED');
        $('#search').click(function() {
            inputs = get_inputs();
            console.log(inputs);
            send_inputs(socket, inputs); 
        });
    });
});
