$(document).ready(function() {
    update = function() {
        var times = $('div.message .timestamp').toArray();
        times.forEach(function(time) {
            $(time).hide().html(moment(new Date($(time).attr('data-timestamp')).toISOString()).fromNow()).fadeIn(1000);
        });
    };

    setInterval(update, 60000);
});