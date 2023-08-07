
var dice = document.getElementById("dice");
var button = document.getElementById("btn");

btn.onclick = function () {
    rollDice();
};

function rollDice() {
    let diceSide = Math.floor(Math.random() * 6 + 1);
    console.log(diceSide);
    for (let i = 1; i <= 6; i++) {
        dice.classList.remove("show-" + i);

        if (diceSide === i) {
            dice.classList.add("show-" + i);
        }
    }
    setTimeout(() => {
        var currentPlayer = players[0]; // Assume player 1 goes first
        players.push(players.shift()); // Rotate players array

        playerMover(currentPlayer, diceSide);
    }, 3000);
}