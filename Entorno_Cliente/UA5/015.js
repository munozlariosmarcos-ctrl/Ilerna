function readNumber() {
    let num;

    while (true) {
        let input = prompt("Introduce un número válido:", 0);

        if (input === null || input === "") {
            return null;
        }

        if (isFinite(input)) {
            num = +input;
            break;
        }
    }
    return num;
}

alert(readNumber());