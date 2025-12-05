let fechaActual = new Date();

console.log(fechaActual.getFullYear());

let diasSemana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
let diaTexto = diasSemana[fechaActual.getDay()];

console.log(diaTexto);