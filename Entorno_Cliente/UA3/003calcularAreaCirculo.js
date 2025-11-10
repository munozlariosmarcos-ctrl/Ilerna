

function calcularAreaCirculo(radio) {
   const area = Math.PI * Math.pow(radio, 2);
   return area;
}

const radio = 5;
console.log("El área del círculo  es: " + calcularAreaCirculo(radio));
