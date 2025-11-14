

function generarFraseAleatoria(palabras) {
    function obtenerPalabraAleatoria(categoria) {
        const lista = palabras[categoria];
        const indiceAleatorio = Math.floor(Math.random() * lista.length);
        return lista[indiceAleatorio];
    }
    const sustantivo = obtenerPalabraAleatoria('sustantivos');
    const verbo = obtenerPalabraAleatoria('verbos');
    const adjetivo = obtenerPalabraAleatoria('adjetivos');
    return `El ${sustantivo} ${verbo} ${adjetivo}.`;
} 
const palabras = {
    sustantivos: ["gato", "perro", "ratón", "elefante"],
    verbos: ["salta", "corre", "duerme", "come"],
    adjetivos: ["rápido", "lento", "grande", "pequeño"]
};
console.log(generarFraseAleatoria(palabras))