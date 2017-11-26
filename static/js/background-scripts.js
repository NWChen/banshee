/*
 * Grabs input values from all inputs on the frontend,
 * and arranges them in a JS object for future processing.
 */
const get_inputs = function() {
    var inputs = {
        username: $('#username').val(),
        nearest_location: $('#location').val(),
        mile_radius: $('#mile_radius').val(),
        any_words: $('#any_words').val(),
        all_words: $('#all_words').val(),
        exact_phrase: $('#exact_phrase').val()
    };
    return inputs;
};

/*
 * Whenever the user edits values in the input boxes on the frontend,
 * those values are sent via WebSockets to the server for processing.
 */
const send_inputs = function(socket, inputs) {
    socket.emit('inputs', inputs);
};

/*
 * Update the tweet feed in `templates/index.html`.
 * Uses Handlebars expressions to dynamically update content.
 * The template for this content is built into `index.html`.
 */
const update_template = function(data, template) {
    var context = {
        'name': data['name'],
        'text': data['text'],
        'timestamp': data['timestamp'],
        'id_str': data['id_str']
    };
    var compiled_html = template(context);
    $('.content-placeholder').html(compiled_html);
};

$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stream');
    var template = Handlebars.compile($('#address-template').html());

    /*
     * If WebSocket connection between client and server fails, we have a problem,
     * and the app cannot function.
     * TODO handle this case
     */
    socket.on('connect', function() {

        /*
         * Handle behaviors on clicking the 'SEARCH' button.
         * TODO enable this behaviors when 'enter' is pressed as well.
         * Sends values of all input boxes to the receiving WebSocket on the server.
         */
        $('#search').click(function() {
            send_inputs(socket, get_inputs()); 
        });

        /*
         * Handle behaviors upon receiving data from the server.
         * This happens asynchronously, i.e. no signals for data are sent from the client to the server.
         * TODO make this actually true via streaming data
         */
        socket.on('data', function(data) {
            update_template(data, template);
        });
    });
});
