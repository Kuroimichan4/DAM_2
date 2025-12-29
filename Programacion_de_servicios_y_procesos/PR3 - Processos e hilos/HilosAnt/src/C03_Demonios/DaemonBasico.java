package C03_Demonios;

public class DaemonBasico {
    public static void main(String[] args) throws InterruptedException {
        String m = "MHN ";
        Thread daemon = new Thread(() -> {
            int i = 0;
            
            while (true) {
                System.out.println(m + "[DAEMON] trabajando... " + i++);
                try {
                    Thread.sleep(500); // medio segundo
                } catch (InterruptedException e) {
                    System.out.println(m + "[DAEMON] interrumpido");
                    break;
                }
            }
        });
        // Lo marcamos como hilo demonio ANTES de arrancarlo
        daemon.setDaemon(true); // el true o el false indica si está ligado el thread al padre o no, por lo tanto si el main se cortsa el hijo también si está ligado
        System.out.println(m + "¿daemon.isDaemon()? " + daemon.isDaemon()); // true
        daemon.start();
        // El hilo main sigue con su vida
        System.out.println(m + "[MAIN] voy a dormir 2 segundos");
        Thread.sleep(2000);
        System.out.println(m + "[MAIN] termino ahora. La JVM se apagará y matará al daemon.");
    }
}
