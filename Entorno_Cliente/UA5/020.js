function checkSpam(str) {
    let lowerStr = str.toLowerCase();
    return lowerStr.includes('viagra') || lowerStr.includes('xxx');
}

alert( checkSpam('compra ViAgRA ahora') );
alert( checkSpam('xxxxx gratis') );
alert( checkSpam("coneja inocente") );