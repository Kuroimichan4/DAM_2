package C02_SleepYieldSetPriority;

public class DemoSleepYieldPriority {
    private static String m = "MHN ";
    // ====== DEMO 1: sleep() ======
    static class SleepTask implements Runnable { //tener una clase que hereda de runnable obliga a tener dentro un metodo public void run()
        
        private final String name;
        private final int delay; // esto indicará el tiempo que se pone a dormiur. Se define en el main
        public SleepTask(String name, int delay) {
            this.name = name;
            this.delay = delay;
        }
        @Override
        public void run() {
            System.out.println(m + "[" + name + "] empieza");
            for (int i = 1; i <= 5; i++) {
                System.out.println(m + "[" + name + "] paso " + i);
                try {
                    Thread.sleep(delay); // se duerme 'delay' milisegundos
                } catch (InterruptedException e) {
                    System.out.println(m + "[" + name + "] interrumpido");
                }
            }
            System.out.println(m + "[" + name + "] termina");
        }
    }
    // ====== DEMO 2: yield() ======
    static class YieldTask implements Runnable { // el Yiel es un método estático de Thread que indica que no está haciendo nada urgente y le puede dar prioridad a otro hilo
        private final String name;
        private final boolean useYield; // esto es un boolean que indicará si tiene proridad o no
        public YieldTask(String name, boolean useYield) {
            this.name = name;
            this.useYield = useYield;
        }
        @Override
        public void run() {
            System.out.println(m + "{" + name + "} empieza");
            for (int i = 1; i <= 20; i++) {
                System.out.println(m + "{" + name + "} i=" + i);
                // Hacemos algo de "trabajo" tonto
                for (int j = 0; j < 1_000_00; j++) { // esto lo único que hace es que la CPU cuente hasta 100000 para hacrlo laburar
                    // ocupamos CPU
                }
                if (useYield && i % 3 == 0) { // si es divisible entre 3 y el resto es 0, se ejecuta
                    System.out.println(m + "{" + name + "} hace yield()"); // el yield es solo una sugerencia de ceder el turno a otro hilo
                    Thread.yield(); // sugiere ceder la CPU
                }
            }
            System.out.println(m + "{" + name + "} termina");
        }
    }
    // ====== DEMO 3: setPriority() ======
    static class PriorityTask implements Runnable {
        private final String name;
        public PriorityTask(String name) {
            this.name = name;
        }
        @Override
        public void run() {
            long start = System.currentTimeMillis();
            long sum = 0;
            for (int i = 0; i < 50_000_000; i++) {
                sum += i;
                if (i % 10_000_000 == 0) {
                    System.out.println(m + "[" + name + "] i=" + i);
                }
            }
            long end = System.currentTimeMillis();
            System.out.println(m + "[" + name + "] termina en " + (end - start) + " ms (sum=" + sum + ")");
        }
    }
    public static void main(String[] args) throws InterruptedException {
        // =============================
        // DEMO 1: sleep()
        // =============================
        System.out.println("======= DEMO SLEEP =======");
        Thread s1 = new Thread(new SleepTask("Lento", 400)); // duerme más. Esto crea el hilo y la tarea
        Thread s2 = new Thread(new SleepTask("Rápido", 200)); // duerme menos
        s1.start(); //esto lo inicia
        s2.start();
        s1.join();
        s2.join();
        // =============================
        // DEMO 2: yield()
        // =============================
        System.out.println("\n======= DEMO YIELD =======");
        Thread y1 = new Thread(new YieldTask("SinYield", false));
        Thread y2 = new Thread(new YieldTask("ConYield", true));
        y1.start();
        y2.start();
        y1.join();
        y2.join();
        // =============================
        // DEMO 3: setPriority()
        // =============================
        System.out.println("\n======= DEMO PRIORITY =======");
        Thread p1 = new Thread(new PriorityTask("Prioridad_Baja"));
        Thread p2 = new Thread(new PriorityTask("Prioridad_Media"));
        Thread p3 = new Thread(new PriorityTask("Prioridad_Alta"));
        // Prioridades (1 a 10)
        p1.setPriority(Thread.MIN_PRIORITY);   // 1
        p2.setPriority(Thread.NORM_PRIORITY);  // 5
        p3.setPriority(Thread.MAX_PRIORITY);   // 10
        System.out.println(m + "Prioridad_Baja = " + p1.getPriority());
        System.out.println(m + "Prioridad_Media = " + p2.getPriority());
        System.out.println(m + "Prioridad_Alta = " + p3.getPriority());
        p1.start();
        p2.start();
        p3.start();
        p1.join();
        p2.join();
        p3.join();
        System.out.println("\n" + m +  "Fin de todas las demos");
    }
}
