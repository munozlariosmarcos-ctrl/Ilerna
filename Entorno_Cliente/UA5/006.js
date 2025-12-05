let estudiante = {
    nombre: "Ana",
    edad: 20,
    carrera: "Informática",
    mostrarInfo: function() {
        console.log(`Estudiante: ${this.nombre}, Edad: ${this.edad}, Carrera: ${this.carrera}`);
    }
};

estudiante.mostrarInfo();

estudiante.edad = 21;
estudiante.mostrarInfo();