function esPalindromo(cadena) {
    const limpia = cadena.toLowerCase().replace(/[^a-z0-9]/g, '');
    const invertida = limpia.split('').reverse().join('');
    return limpia === invertida;
}
console.log(esPalindromo("Ana")); 