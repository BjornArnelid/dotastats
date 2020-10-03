"use strict";
$(document).on('submit', 'form', function(e) {
	$.ajax({
		url: $(this).attr('action'),
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		type: $(this).attr('method'),
		data: $(this).serialize(),
		success: function(result) {
			$("table tBody").empty()
			var bestPicks = result['picks'].slice(0,result['picks'].length/2);
			var bestBans = result['bans'].slice(0,result['bans'].length/2);
			for(var i=0; i < 5; i++) {
			    var pickString = "<td/>";
			    var banString = "<td/>";
			    var pick = bestPicks[i];
			    if (pick) {
				    var pickString = `<td id="${pick.hero_id}"><img src="${pick.icon}" alt="${pick.name}"> ${pick.name}   Games:${pick.games}  Win:${Math.round(pick.winrate)}% </td>`;
				}

				var ban = bestBans[i];
				if (ban) {
				    var banString = `<td id="${ban.hero_id}"><img src="${ban.icon}" alt="${ban.name}"> ${ban.name}   Games:${ban.against_games}  Win:${Math.round(ban.against_winrate)}% </td>`;
				}
			    var row = "<tr>" + pickString + banString + "</tr>";
				$("#best").find("tBody").append(row);
			}

			var worstPicks = result['picks'].reverse().slice(0,result['picks'].length/2);
			var worstBans = result['bans'].reverse().slice(0,result['bans'].length/2);
			for(var i=0; i < 5; i++) {
			    var pickString = "<td/>";
			    var banString = "<td/>";
			    var pick = worstPicks[i];
			    if (pick) {
				    var pickString = `<td id="${pick.hero_id}"><img src="${pick.icon}" alt="${pick.name}"> ${pick.name}   Games:${pick.games}  Win:${Math.round(pick.winrate)}% </td>`;
				}

				var ban = worstBans[i];
				if (ban) {
				    var banString = `<td id="${ban.hero_id}"><img src="${ban.icon}" alt="${ban.name}"> ${ban.name}   Games:${ban.against_games}  Win:${Math.round(ban.against_winrate)}% </td>`;
				    var row = "<tr>" + pickString + banString + "</tr>";
				}
				$("#worst").find("tBody").append(row);
			}

		}
	}, 'json');
	e.preventDefault();
});

$(document).ready(function(){
	$("table tBody").on('click', 'td', function(e) {
        var hero_id = $(e.target).attr('id');
        $("#heroPick").val(hero_id);
	    $("#submitForm").submit();
	///{{id}}/synergies/{{picks[i].hero_id}}?{{query}}

	});
});

$.getJSON("/heroes", function(data) {
    for (var h in data) {
        $("#heroPick").append(new Option(data[h].localized_name, h));
    }
});

