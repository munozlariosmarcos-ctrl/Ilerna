let id = Symbol("id");
let empleado = {
  nombre: "Lucía",
  [id]: 123
};

for (let clave in empleado) {
  console.log(clave); 
}