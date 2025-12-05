let listaNumeros = [10, 20, 30, 40, 50];

let sumaTotal = listaNumeros.reduce((acumulador, valorActual) => acumulador + valorActual, 0);
console.log(sumaTotal);

let productoTotal = listaNumeros.reduce((acumulador, valorActual) => acumulador * valorActual, 1);
console.log(productoTotal);