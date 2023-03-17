let canvasSize = 300;

function updateCanvasCell(cellWidth, canvas, event) {
	const rect = canvas.getBoundingClientRect()
	x = Math.floor((event.clientX - rect.left) / cellWidth);
	y = Math.floor((event.clientY - rect.top) / cellWidth);
	// console.log("x: " + x + " y: " + y);

	let color = document.getElementById("inputColor").value;
	color = color.replace('#', '');
	console.log(color);

	fetch("pixel/set", {
		method: "post",
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		//make sure to serialize your JSON body
		body: JSON.stringify({
			"x": x,
			"y": y,
			"color": color,
			"user": "fauwara",
		})
		// body: `x=${x}&y=${y}&color=${color}&user=fauwara`
	})
		.then((response) => {
			console.log(response);

			fetch('canvas')
				.then(response => response.json())
				.then(result => {

					let canvasHeight = result.size[0];
					let canvasWidth = result.size[1];

					let cellWidth = canvasSize / canvasWidth;

					displayCanvas(canvasHeight, canvasWidth, cellWidth, result.data);
				});
		});
}

function displayCanvas(height, width, cellWidth, data) {

	let count = 0;
	for (let i = 0; i < height; i++) {
		for (let j = 0; j < width; j++) {
			ctx.fillStyle = "#" + data[j][i];
			ctx.fillRect(0 + (j * cellWidth), 0 + (i * cellWidth), cellWidth, cellWidth);
			count++;
		}
	}

};

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

fetch('canvas')
	.then(response => response.json())
	.then(result => {

		let canvasHeight = result.size[0];
		let canvasWidth = result.size[1];

		let cellWidth = canvasSize / canvasWidth;

		displayCanvas(canvasHeight, canvasWidth, cellWidth, result.data);

		canvas.addEventListener('mousedown', function (e) {
			updateCanvasCell(cellWidth, canvas, e);
		})

	});

function signUp() {
	const username = document.getElementById('username-signup').value;
	const password = document.getElementById('password-signup').value;

	fetch("signup", {
		method: "post",
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		//make sure to serialize your JSON body
		body: JSON.stringify({
			"username": username,
			"password": password,
		})
		// body: `x=${x}&y=${y}&color=${color}&user=fauwara`
	})
		.then((response) => {
			console.log(response);
		});
}