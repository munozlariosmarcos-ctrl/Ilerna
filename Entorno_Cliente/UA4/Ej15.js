class Vehiculo {
  constructor(marca) {
    this.marca = marca;
  }

  arrancar() {
    console.log(`El vehículo de marca ${this.marca} está arrancando.`);
  }
}

class Coche extends Vehiculo {
  constructor(marca, modelo) {
    super(marca);
    this.modelo = modelo;
  }

  arrancar() {
    console.log(`El coche ${this.marca} ${this.modelo} está arrancando.`);
  }

  detener() {
    console.log(`El coche ${this.marca} ${this.modelo} se ha detenido.`);
  }
}

let miCoche = new Coche("Toyota", "Corolla");
miCoche.arrancar();
miCoche.detener();