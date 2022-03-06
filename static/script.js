let turn = 1;

const addScore = () => {
	const current = document.getElementById("currentScore" + turn).innerHTML;
	const newScore = document.getElementById("newScore").value;
	const score = current - newScore;
	document.getElementById("currentScore" + turn).innerText = score;
	turn++;
	console.log(turn);
	if (turn >= 3) {
		turn = 1;
	}
}

const showScore = () => {
	console.log("asda");
	const s = document.getElementById("c");
	const bb = document.getElementById("bb");
	bb.style.display = "none";
	s.style.display = "block";
}