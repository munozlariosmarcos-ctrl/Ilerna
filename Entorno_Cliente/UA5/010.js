let empresa = {
    nombre: "Tech Solutions",
    ubicacion: {
        pais: "España",
        ciudad: "Madrid"
    },
    empleados: [
        { nombre: "Carlos", puesto: "Desarrollador" },
        { nombre: "Laura", puesto: "Diseñadora" }
    ]
};

console.log(empresa.ubicacion.ciudad);

empresa.empleados.push({ nombre: "Pedro", puesto: "Gerente" });

console.log(empresa.empleados);