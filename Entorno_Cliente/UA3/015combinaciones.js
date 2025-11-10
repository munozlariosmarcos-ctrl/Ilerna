function combinaciones(cadena) {
    const resultado = [];
    function generar(prefix, resto) {
        for (let i = 0; i < resto.length; i++) {
            const nueva = prefix + resto[i];
            resultado.push(nueva);
            generar(nueva, resto.slice(i + 1));
        }
    }
    generar('', cadena);
    return resultado;
}
console.log(combinaciones("abc"));