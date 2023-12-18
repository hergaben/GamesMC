let btn = document.getElementById('gen_btn');
let thumbnail = document.getElementById('thumbnail');
let game_name = document.getElementById('name_game');
let description_game = document.getElementById('description_game');
let genre_game = document.getElementById('genre_game');
let release_date = document.getElementById('release_date');

let current = 0;

btn.onclick = async function() {
    fetch("http://localhost:80/")
        .then((response) => response.json())
        .then((data) => {
            current = data["id"];
            thumbnail.src = data['thumbnail'];
            game_name.textContent = data['title'];
            description_game.innerHTML = data['description'];
            genre_game.textContent = data['genre'];
            release_date.textContent = data['release_date'];
        });
};

let add = document.getElementById('add');

add.onclick = async function() {
    fetch("http://localhost:3001/?id=" + current.toString(), {
        method: "POST"
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
};
