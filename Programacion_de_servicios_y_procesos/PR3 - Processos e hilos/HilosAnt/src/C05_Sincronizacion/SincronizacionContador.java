package C05_Sincronizacion;

public class SincronizacionContador {
    private static String m = "MHN ";
    // ======= RECURSO COMPARTIDO =======
    static class Contador {
        private int valor = 0;
        // Versión SIN sincronizar (descomentar para probar)
        
        public void incrementar() {
            valor++; // NO es atómico
        } // lo de atómico es que se hace lo de leer, sumar y guardar a la vez. Que es un paso indivisible y en este caso no lo es
        // lo que puede hacer que los 2 hilos lo llamen a la vez y lo sumen a la vez y se puierda uno de los incrementos por ejemplo
         
        // Versión CON sincronización
//        public synchronized void incrementar() {
//            valor++; // ahora este incremento es atómico respecto a otros hilos
//        }
        public int getValor() {
            return valor;
        }
    }
    // ======= TAREA DEL HILO =======
    static class TareaIncremento implements Runnable {
        private final Contador contador;
        private final int repeticiones;
        public TareaIncremento(Contador contador, int repeticiones) {
            this.contador = contador;
            this.repeticiones = repeticiones;
        }
        @Override
        public void run() {
            for (int i = 0; i < repeticiones; i++) {
                contador.incrementar();
            }
        }
    }
    public static void main(String[] args) throws InterruptedException {
        Contador contador = new Contador();
        int repeticiones = 1_000_000;
        Thread t1 = new Thread(new TareaIncremento(contador, repeticiones), "Hilo-1");
        Thread t2 = new Thread(new TareaIncremento(contador, repeticiones), "Hilo-2");
//        Thread t3 = new Thread(new TareaIncremento(contador, repeticiones), "Hilo-3");
//        Thread t4 = new Thread(new TareaIncremento(contador, repeticiones), "Hilo-4");
//        Thread t5 = new Thread(new TareaIncremento(contador, repeticiones), "Hilo-5");
        long inicio = System.currentTimeMillis();
        t1.start();
        t2.start();
//        t3.start();
//        t4.start();
//        t5.start();
        t1.join(); // esto es para que no siga con el programa hasta que hayan terminado los 2 hilos
        t2.join();
//        t3.join();
//        t4.join();
//        t5.join();
        long fin = System.currentTimeMillis();
        System.out.println(m + "Valor esperado: " + (2 * repeticiones));
        System.out.println(m + "Valor real:     " + contador.getValor());
        System.out.println(m + "Tiempo: " + (fin - inicio) + " ms");
    }
}
