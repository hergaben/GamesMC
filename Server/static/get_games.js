let container = document.getElementById('game_container');

fetch("http://localhost:3001/").then((Response) => {
        return Response.json()
    }).then((data) => {
        for (let index = 0; index < data.length; index++) {
            data[index] = 'q=' + data[index] + '&';

        }
        console.log(data.join(''));

        fetch("http://localhost:80/list/?" + data.join('')).then((Response) => {
                return Response.json()
            }).then((data) => {
                console.log(data);
                data.forEach(element => {
                    container.innerHTML += '<div class="imdbID">' +
                '<h2 class="name">' + element["title"] + '</h2>' +
                '<img class="image" src="' + element["thumbnail"] + '" alt="Game Image">' +
                '</div>';

                });
            });
    })


