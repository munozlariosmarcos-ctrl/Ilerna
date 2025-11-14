
function calcularPermutaciones(array) { 
    if (array.length === 0) return [[]];
    const resultado = [];
    for (let i = 0; i < array.length; i++) {
        const elementoActual = array[i];
        const elementosRestantes = array.slice(0, i).concat(array.slice(i + 1));
        const permutacionesRestantes = calcularPermutaciones(elementosRestantes);
        for (const permutacion of permutacionesRestantes) {
            resultado.push([elementoActual, ...permutacion]);
        }
    }
    return resultado;
}
console.log(calcularPermutaciones([1, 2, 3]));
console.log(calcularPermutaciones(['a', 'b', 'c']));