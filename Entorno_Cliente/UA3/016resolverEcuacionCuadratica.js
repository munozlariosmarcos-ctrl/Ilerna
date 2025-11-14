
function resolverEcuacionCuadratica(a, b, c) {
    const discriminante = b * b - 4 * a * c;
    if (discriminante < 0) {
        return "No hay raíces reales";
    } else {
        const raiz1 = (-b + Math.sqrt(discriminante)) / (2 * a);
        const raiz2 = (-b - Math.sqrt(discriminante)) / (2 * a);
        return [raiz1, raiz2];
    }
}

console.log(resolverEcuacionCuadratica(1, -3, 2)); 
console.log(resolverEcuacionCuadratica(1, 2, 5));  
