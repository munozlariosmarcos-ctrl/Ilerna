function factorial(n) {
    if (n < 0) return undefined;
    let resultado = 1;
    for (let i = 2; i <= n; i++) {
        resultado *= i;
    }
    return resultado;
}
console.log(factorial(5));