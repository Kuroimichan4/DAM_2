package C03_Demonios;

public class DaemonHerencia {
    public static void main(String[] args) throws InterruptedException {
        String m = "MHN ";
        System.out.println(m + "[MAIN] isDaemon = " + Thread.currentThread().isDaemon()); // false
        Thread noDaemon = new Thread(() -> {
            System.out.println(m + "[NO-DAEMON] isDaemon = " + Thread.currentThread().isDaemon());
            // Hilo creado desde un hilo normal (no daemon)
            Thread hijo = new Thread(() -> {
                System.out.println(m + "[HIJO DE NO-DAEMON] isDaemon = " + Thread.currentThread().isDaemon());
            });
            hijo.start();
            try {
                hijo.join();
            } catch (InterruptedException e) {
            }
        });
        Thread daemon = new Thread(() -> {
            System.out.println(m + "[DAEMON] isDaemon = " + Thread.currentThread().isDaemon());
            // Hilo creado desde un hilo daemon
            Thread hijo = new Thread(() -> {
                System.out.println(m + "[HIJO DE DAEMON] isDaemon = " + Thread.currentThread().isDaemon());
            });
            hijo.start();
            try {
                hijo.join();
            } catch (InterruptedException e) {
            }
        });
        daemon.setDaemon(true); // esto es lo que indica sies daemon o no
        noDaemon.start();
        daemon.start();
        //daemon.setDaemon(false); // cambio la caracteristica después de iniciarlo a true
        noDaemon.join();
        daemon.join();
        System.out.println(m + "[MAIN] fin");
    }
}
