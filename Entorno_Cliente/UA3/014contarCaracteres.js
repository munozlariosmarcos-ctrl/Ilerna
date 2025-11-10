function contarCaracteres(cadena) {
    const conteo = {};
    for (let char of cadena.replace(/\s/g, '')) {
        conteo[char] = (conteo[char] || 0) + 1;
    }
    return conteo;
}
console.log(contarCaracteres("Hola Mundo"));