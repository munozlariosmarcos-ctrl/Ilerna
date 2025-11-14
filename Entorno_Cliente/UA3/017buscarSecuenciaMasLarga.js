

function buscarSubsecuenciaMasLarga(cadena1, cadena2) {
    const m = cadena1.length;
    const n = cadena2.length;
    const tabla = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (cadena1[i - 1] === cadena2[j - 1]) {
                tabla[i][j] = tabla[i - 1][j - 1] + 1;
            }
            else {
                tabla[i][j] = Math.max(tabla[i - 1][j], tabla[i][j - 1]);
            }
        }
    }
    let i = m, j = n;
    let subsecuencia = '';
    while (i > 0 && j > 0) {
        if (cadena1[i - 1] === cadena2[j - 1]) {
            subsecuencia = cadena1[i - 1] + subsecuencia;
            i--;
            j--;
        }
        else if (tabla[i - 1][j] > tabla[i][j - 1]) {
            i--;
        }
        else {
            j--;
        }
    }
    return subsecuencia;
}
console.log(buscarSubsecuenciaMasLarga("ABCBDAB", "BDCAB"));
console.log(buscarSubsecuenciaMasLarga("AGGTAB", "GXTXAYB"));
console.log(buscarSubsecuenciaMasLarga("AAAA", "AA"));
console.log(buscarSubsecuenciaMasLarga("ABCDGH", "AEDFHR"));