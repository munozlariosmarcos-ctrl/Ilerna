let persona = {
  nombre: "Ana",
  edad: 28,
  trabajo: "Ingeniera"
};

for (let clave in persona) {
  console.log(`${clave}: ${persona[clave]}`);
}