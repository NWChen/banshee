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

const send_inputs = function(socket, inputs) {
    socket.emit('inputs', inputs);
};

const format_data = function(data, keyword) { // TODO - handle multiple keywords
    data = JSON.parse(data);
    var contents = data['content'];
    var id = data['url'];
    data['url'] = id.substring(id.lastIndexOf('/'))
    var tag_start = '<span class=\"keyword\">'
    var tag_end = '</span>';

    contents = contents.replace(new RegExp(keyword, 'g'), tag_start + keyword + tag_end);
    data['content'] = contents;
    return data; // an Object with the same fields as the parameter data
};

const setup_listeners = function(socket) {
    // Client event handlers
    $('#search').click(function() {
        send_inputs(socket, get_inputs()); 
    });

    // Socket event handlers
    socket.on('data', function(data) {
        tweet_html = format_data(data['data'], data['keywords']);
        $('.content').html(tweet_html['content']);
        //$('#data').html(data['data']);
    });
}

$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stream');
    socket.on('connect', function() {
        setup_listeners(socket);
    });
});
