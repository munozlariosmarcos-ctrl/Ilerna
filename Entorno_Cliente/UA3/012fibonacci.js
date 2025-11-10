function fibonacci(n) {
    if (n <= 0) return [];
    const secuencia = [0];
    if (n === 1) return secuencia;
    secuencia.push(1);
    for (let i = 2; i < n; i++) {
        secuencia.push(secuencia[i - 1] + secuencia[i - 2]);
    }
    return secuencia;
}
console.log(fibonacci(7));