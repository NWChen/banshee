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
 * Highlight tokens in content.
 */
const highlight = function(html, tokens) {
    pre_tag = '<span class=\'highlight\'>';
    post_tag = '</span>';
    for(var i=0; i<tokens.length; i++) {
        html = html.toLowerCase().replace(tokens[i], pre_tag + tokens[i] + post_tag);
    }
    return html;
};

/*
 * Generate an array of tokens to highlight from an inputs dictionary.
 */
const get_desirable_tokens = function(inputs) {
    tokens = [];
    Object.keys(inputs).forEach(function(key) {
        Array.prototype.push.apply(tokens, inputs[key].split(','));
    });
    return tokens;
};

/*
 * Update the tweet feed in `templates/index.html`.
 * Uses Handlebars expressions to dynamically update content.
 * The template for this content is built into `index.html`.
 */
const update_template = function(data, template) {
    var context = {
        'tweets': data
    };
    console.log(data)
    var compiled_html = template(context);
    return compiled_html;
};

$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stream');
    var inputs = {};
    var template = Handlebars.compile($('#data-template').html());
    var RESPONSE_TIMEOUT = 500;

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
            console.log('SEARCH PRESSED');
            inputs = get_inputs();
            send_inputs(socket, inputs); 
        });

        /*
         * Handle behaviors upon receiving data from the server.
         * Loop this behavior by asking for more data from the server.
         */
        socket.on('data', function(data) {
            console.log(data);
            // Update streaming button
            $('[data-loading-start]').removeClass('hide');
            $('[data-loading-end]').addClass('hide');
            $('[data-success-message]').removeClass('hide');

            // Update tweet queue 
            compiled_html = update_template(data, template);
            compiled_html = highlight(compiled_html, get_desirable_tokens(inputs));
            $('.content-placeholder').html(compiled_html);
            setTimeout(function() {
                socket.emit('more'); // Ask for more data from the server.
            }, RESPONSE_TIMEOUT);
        });
    });
});
