let cuentaBancaria = {
  saldo: 1000,
  toString() {
    return `Saldo: ${this.saldo} EUR`;
  }
};

console.log(cuentaBancaria.toString()); 