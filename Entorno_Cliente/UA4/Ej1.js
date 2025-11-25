let persona={
    nombre:"Ana",
    edad:28,
    trabajo:"Ingenieria"
}

console.log("Nombre :" , persona.nombre)
console.log("Edad :" , persona.edad)


persona.pais="España"
delete persona.trabajo

console.log("Objeto completo : " , persona)

let producto = "manzanas"

let carrito={
    [producto]:10
}
console.log("Carrito" , carrito)

let nuevoProducto = "peras";
carrito[nuevoProducto] = 5;

console.log("Carrito actualizado : " , carrito);

if ("nombre" in persona) {
    console.log("La propiedad 'nombre' existe en persona.");
} else {
  console.log("La propiedad 'nombre' NO existe en persona.");
}

if ("apellido" in persona) {
    console.log("La propiedad 'apellido' existe en persona.");
} else {
  console.log("La propiedad 'apellido' NO existe en persona.");
}

for (let clave in persona){
    console.log("Objeto modificado " + clave + " : " + persona[clave])
}