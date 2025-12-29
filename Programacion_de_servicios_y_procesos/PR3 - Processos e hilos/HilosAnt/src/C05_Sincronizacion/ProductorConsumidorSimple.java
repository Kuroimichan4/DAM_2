package C05_Sincronizacion;

public class ProductorConsumidorSimple {
    private static String m = "MHN ";
    
    // ======= BUFFER COMPARTIDO (MONITOR) =======
    static class Buffer {
        private Integer dato = null; // null = vacío
        public synchronized void poner(int nuevoDato) throws InterruptedException {
            // Mientras esté lleno, el productor espera
            while (dato != null) {
                System.out.println(m + "Intento poner pero datos ya tiene datos");
                wait(); // libera el monitor y se bloquea. Se usa para que ese hilo libere el recurso y otros puedan tomarlo
            }
            // Llegados aquí, el buffer está vacío
            dato = nuevoDato;
            System.out.println(m + Thread.currentThread().getName()
                    + " ha producido: " + nuevoDato);
            // Despertamos a posibles consumidores
            notifyAll();
        }
        public synchronized int tomar() throws InterruptedException {
            // Mientras esté vacío, el consumidor espera
            while (dato == null) {
                System.out.println(m + "Intento tomar pero está vacio");
                wait(); // libera el monitor y se bloquea
            }
            // Llegados aquí, hay un dato disponible
            int resultado = dato;
            dato = null; // vaciamos el buffer
            System.out.println(m + Thread.currentThread().getName()
                    + " ha consumido: " + resultado);
            // Despertamos a posibles productores
            notifyAll();
            return resultado;
        }
    }
    // ======= PRODUCTOR =======
    static class Productor implements Runnable {
        private final Buffer buffer;
        public Productor(Buffer buffer) {
            this.buffer = buffer;
        }
        @Override
        public void run() {
            try {
                for (int i = 1; i <= 10; i++) {
                    Thread.sleep(1000); // simulamos trabajo
                    buffer.poner(i);
                }
            } catch (InterruptedException e) {
                System.out.println(m + "Productor interrumpido");
            }
        }
    }
    // ======= CONSUMIDOR =======
    static class Consumidor implements Runnable {
        private final Buffer buffer;
        public Consumidor(Buffer buffer) {
            this.buffer = buffer;
        }
        @Override
        public void run() {
            try {
                for (int i = 1; i <= 10; i++) {
                    int valor = buffer.tomar();
                    Thread.sleep(2000); // simulamos procesamiento
                }
            } catch (InterruptedException e) {
                System.out.println(m + "Consumidor interrumpido");
                
            }
        }
    }
    public static void main(String[] args) {
        Buffer buffer = new Buffer();
        Thread productor = new Thread(new Productor(buffer), "Productor");
        Thread consumidor = new Thread(new Consumidor(buffer), "Consumidor");
        productor.start();
        consumidor.start();
    }
}
