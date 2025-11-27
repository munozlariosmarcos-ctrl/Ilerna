class CuentaBancaria {
  #saldo;

  constructor(nombreTitular, saldoInicial) {
    this.nombreTitular = nombreTitular;
    this.#saldo = saldoInicial;
  }

  obtenerSaldo() {
    return this.#saldo;
  }

  depositar(monto) {
    if (monto > 0) {
      this.#saldo += monto;
      console.log(`Depósito exitoso. Nuevo saldo: ${this.#saldo} EUR`);
    }
  }

  retirar(monto) {
    if (monto <= this.#saldo) {
      this.#saldo -= monto;
      console.log(`Retiro exitoso. Nuevo saldo: ${this.#saldo} EUR`);
    } else {
      console.log("Fondos insuficientes.");
    }
  }
}

let cuenta = new CuentaBancaria("Juan", 1000);
console.log(`Saldo inicial: ${cuenta.obtenerSaldo()} EUR`);
cuenta.depositar(500);
cuenta.retirar(200);

console.log(cuenta.saldo);  