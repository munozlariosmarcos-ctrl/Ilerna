let usuario1 = { nombre: "Carlos", edad: 30, email: "carlos@mail.com" };
console.log(usuario1); 

let clon = Object.assign({}, usuario1);
clon.nombre = "Pedro";

console.log(usuario1); 
console.log(clon);     