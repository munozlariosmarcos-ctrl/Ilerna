function Coche(marca, modelo, año) {
  this.marca = marca;
  this.modelo = modelo;
  this.año = año;
}

let coche1 = new Coche("Ford", "Focus", 2020);
console.log(coche1);