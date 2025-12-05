let persona = {
  nombre: "Ana",
  edad: 28,
  trabajo: "Ingeniera"
};

persona.saludar = function() {
  console.log(`Hola, soy ${this.nombre} y tengo ${this.edad} años`);
};

persona.saludar();