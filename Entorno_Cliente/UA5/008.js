let productos = [
    { nombre: "Teclado", precio: 15, disponible: true },
    { nombre: "Ratón", precio: 10, disponible: false },
    { nombre: "Monitor", precio: 100, disponible: true },
    { nombre: "USB", precio: 8, disponible: true }
];

let productosFiltrados = productos.filter(p => p.disponible && p.precio < 20);

let nombresProductos = productosFiltrados.map(p => p.nombre);

console.log(nombresProductos);