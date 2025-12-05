
let numero = 42;
let numeroComoString = String(numero); 

console.log("Valor numérico:", numero, "| Tipo:", typeof numero);
console.log("Valor string:", numeroComoString, "| Tipo:", typeof numeroComoString);

let deNuevoNumero = Number(numeroComoString);
console.log("De vuelta a número:", deNuevoNumero, "| Tipo:", typeof deNuevoNumero);