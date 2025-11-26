let persona={
    nombre:"Ana",
    edad:28,
    trabajo:"Ingenieria",
    //09.js
    saludar: function() {
        console.log(`Hola, soy ${this.nombre} y tengo ${this.edad} años`);
    }

}

console.log("Nombre :" , persona.nombre)
console.log("Edad :" , persona.edad)


persona.pais="España"
delete persona.trabajo

console.log("Objeto completo : " , persona)
//07.js
let producto = "manzanas"

let carrito={
    [producto]:10
}
console.log("Carrito" , carrito)

let nuevoProducto = "peras";
carrito[nuevoProducto] = 5;

console.log("Carrito actualizado : " , carrito);
//05.js
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
//06.js
for (let clave in persona){
    console.log("Objeto modificado " + clave + " : " + persona[clave])
}
//08.js
const usuario2 = persona;

usuario2.edad = 30;

console.log("usuario1:", persona);
console.log("usuario2:", usuario2);


const clonUsuario = Object.assign({}, persona);
clonUsuario.nombre = "Laura";

console.log("usuario1:", persona);
console.log("clonUsuario:", clonUsuario);

persona.saludar();


//010.js
// Constructor Coche
function Coche(marca, modelo, año) {
    this.marca = marca;
    this.modelo = modelo;
    this.año = año;


    this.detalles = function() {
        console.log(`Coche: ${this.marca} ${this.modelo}, Año: ${this.año}`);
    };
}

const coche1 = new Coche("Toyota", "Corolla", 2020);
const coche2 = new Coche("Ford", "Focus", 2018);

console.log(coche1);
console.log(coche2);

coche1.detalles();
coche2.detalles();

//011.js
const id = Symbol("id");
let empleado = {
    nombre: "Carlos",
    puesto: "Desarrollador"
};

empleado[id] = 12345;
for (let clave in empleado) {
    console.log(clave + " : " + empleado[clave]);
}
console.log("ID del empleado:", empleado[id]);

//012.js
let cuentaBancaria = {
    saldo: 1000,

    toString: function() {
        return `Saldo: ${this.saldo} EUR`;
    }
};
console.log(cuentaBancaria.toString());
console.log(String(cuentaBancaria));  