// assets/js/aflvis.js

$( document ).ready(function() {


    var years = ['2011', '2012', '2013', '2014'];
    var rounds = new Array(24);
    for(var i=0; i<rounds.length; i++) rounds[i] = i+1;
    var teams = ['Hawthorn', 'Geelong', 'Sydney', 'Fremantle', 'Richmond', 'North Melbourne',
                 'Collingwood', 'Adelaide', 'Essendon', 'Carlton', 'Port Adelaide', 'West Coast',
                 'Gold Coast', 'Brisbane Lions', 'Western Bulldogs', 'St Kilda', 'Melbourne',
                 'Greater Western Sydney'];

    $.each(years, function(i, s){
        var optionString = '<option value=' + i + '>' + s + '</option>';
        //console.log(optionString);
        $('#year').append(optionString);
    });

    $.each(rounds, function(i, s){
        var optionString = '<option value=' + i + '>' + s + '</option>';
        //console.log(optionString);
        $("#round").append(optionString);
    });

    $.each(teams, function(i, s){
        var optionString = '<option value=' + i + '>' + s + '</option>';
        //console.log(optionString);
        $("#team").append(optionString);
    });



    // initialize the console and the Handler
    var C = new Console($("#console"));
    var F = new Figure($("#figs"));
    var Handler = new WebSocketHandler(C, F);
    
    // load the saved serverURI into the serveruri input
    //var server = localStorage.getItem(KEY_SERVER_URI);


    var server = "ws://localhost:9999/ws";
    console.log(server);

    var Socket = new WebSocketClient(server, Handler);

    $("#summary").click(function(e) {
        var year = years[$("#year").val()];

        var message = ['graph:', 'summary', year, 'None'].join(' ');
        Socket.send(message);
        e.preventDefault();
    });

    $("#plotgame-all").click(function(e) {
        var year = years[$("#year").val()];

        var message = ['graph:', 'all', year, 'None'].join(' ');
        Socket.send(message);
        e.preventDefault();
    });

    $("#plotgame-round").click(function(e) {
        var year = years[$("#year").val()];
        var round = rounds[$("#round").val()];

        var message = ['graph:', 'round', year, round].join(' ');
        Socket.send(message);
        e.preventDefault();
    });

    $("#plotgame-final").click(function(e) {
        var year = years[$("#year").val()];

        var message = ['graph:', 'final', year, 'None'].join(' ');
        Socket.send(message);
        e.preventDefault();
    });

    $("#plotgame-team1").click(function(e) {
        var year = years[$("#year").val()];
        var team = teams[$('#team').val()];

        var message = ['graph:', 'team1', year, team].join(' ');
        Socket.send(message);
        e.preventDefault();
    });

    $("#plotgame-team2").click(function(e) {
        var year = years[$("#year").val()];
        var team = teams[$('#team').val()];

        var message = ['graph:', 'team2', year, team].join(' ');
        Socket.send(message);
        e.preventDefault();
    });
});
