class Animal {
  constructor(nombre) {
    this.nombre = nombre;
  }

  hacerSonido() {
    console.log(`${this.nombre} está haciendo un sonido.`);
  }
}

class Perro extends Animal {
  constructor(nombre, raza) {
    super(nombre);
    this.raza = raza;
  }

  hacerSonido() {
    console.log(`${this.nombre} está ladrando.`);
  }

  info() {
    console.log(`Nombre: ${this.nombre}, Raza: ${this.raza}`);
  }
}

let miPerro = new Perro("Rex", "Pastor Alemán");
miPerro.hacerSonido();
miPerro.info();