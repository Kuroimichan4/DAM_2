package C04_GruposHilos;

public class EjemploGruposHilos {
    private static String m = "MHN ";
    // Tarea genérica para los hilos
    static class Tarea implements Runnable {
        private final String nombreTarea;
        public Tarea(String nombreTarea) { // Las tareas serán la A, B y C dependiendo del grupo al que pertenezcan
            this.nombreTarea = nombreTarea;
        }
        @Override
        public void run() {
            Thread hiloActual = Thread.currentThread();
            ThreadGroup grupo = hiloActual.getThreadGroup();
            for (int i = 1; i <= 5; i++) { // Sale el nombre del grupo, el nombre del hilo, la tarea y la iteración
                System.out.println(
                        m
                        + "[" + grupo.getName() + "] "
                        + hiloActual.getName()
                        + " - " + nombreTarea
                        + " - iteración " + i
                );
                try {
                    Thread.sleep(400); // un poco de tiempo para ver el intercalado
                } catch (InterruptedException e) {
                    System.out.println(m + hiloActual.getName() + " interrumpido");
                    return;
                }
            }
            System.out.println(m + "[" + grupo.getName() + "] " + hiloActual.getName() + " ha terminado.");
        }
    }
    public static void main(String[] args) throws InterruptedException {
        // ====== 1. Creación de grupos ======
        ThreadGroup grupoPadre = new ThreadGroup("Grupo Padre"); // crea el grupo padre
        ThreadGroup subgrupo = new ThreadGroup(grupoPadre, "Grupo Hijo"); //crea el subgrupo Grupo hijo
        System.out.println(m + "Grupo padre: " + grupoPadre.getName());
        System.out.println(m + "Subgrupo: " + subgrupo.getName());
        System.out.println(m + "Padre del subgrupo: " + subgrupo.getParent().getName());
        // ====== 2. Creación de hilos dentro de los grupos ======
        Thread hilo1 = new Thread(grupoPadre, new Tarea("Tarea A"), "Hilo-A (padre)"); // crea un hilo dentro del grupo padre
        Thread hilo2 = new Thread(grupoPadre, new Tarea("Tarea B"), "Hilo-B (padre)"); // grupo padre
        Thread hilo3 = new Thread(subgrupo, new Tarea("Tarea C"), "Hilo-C (hijo)"); //subgrupo hijo
//        Thread hiloDefault = new Thread(new Tarea("Tarea Default"), "Hilo-Default"); //hilo Default que se asigna al main ya que no se le da grupo
        // (Ejemplo con lambda equivalente, por si quieres enseñarlo)
        // Thread hiloLambda = new Thread(grupoPadre, () -> {
        //     System.out.println("Soy un hilo con lambda en " +
        //             Thread.currentThread().getThreadGroup().getName());
        // }, "Hilo-Lambda");
        // ====== 3. Arrancar los hilos ======
        hilo1.start();
        hilo2.start();
        hilo3.start();
//        hiloDefault.start();
        // hiloLambda.start();
        // Esperamos un poco para asegurarnos de que ya han arrancado
        Thread.sleep(200);
        // ====== 4. Información de grupos mientras los hilos están activos ======
        System.out.println("\n--- Info de grupos mientras los hilos están activos ---");
        System.out.println(m + "Hilos activos en grupoPadre (solo ese grupo): " + grupoPadre.activeCount());
        System.out.println(m + "Subgrupos activos dentro de grupoPadre: " + grupoPadre.activeGroupCount());
        // Lista de hilos dentro de grupoPadre (sin recorrer subgrupos)
        Thread[] listaHilos = new Thread[grupoPadre.activeCount()]; //esto cuenta los hilos del grupo padre sin contar los hijos xq está en false
        int numHilos = grupoPadre.enumerate(listaHilos, false); // false = no incluir subgrupos
        System.out.println("\n--- Hilos encontrados en grupoPadre (sin subgrupos):");
        for (int i = 0; i < numHilos; i++) {
            Thread t = listaHilos[i];
            System.out.println(m + "- " + t.getName() + " (grupo: " + t.getThreadGroup().getName() + ")");
        }
        // Lista de subgrupos dentro de grupoPadre
        ThreadGroup[] listaGrupos = new ThreadGroup[grupoPadre.activeGroupCount()]; //esto cuenta los grupos hijo activos
        int numGrupos = grupoPadre.enumerate(listaGrupos, false);
        System.out.println("\nSubgrupos dentro de grupoPadre:");
        for (int i = 0; i < numGrupos; i++) {
            ThreadGroup tg = listaGrupos[i];
            System.out.println(m + "- " + tg.getName());
        }
//        System.out.println("\n--- Hilo sin Grupo ");
//        System.out.println(m + "- Hilo default: " + hiloDefault.getThreadGroup().getName());
        
        // ====== 5. Prioridades a nivel de grupo ======
        System.out.println("\n--- Prioridades y grupos ---");
        System.out.println(m + "Prioridad máxima inicial del subgrupo: " + subgrupo.getMaxPriority());
        subgrupo.setMaxPriority(4); // fijamos prioridad máxima del subgrupo en 4
        System.out.println(m + "Nueva prioridad máxima del subgrupo: " + subgrupo.getMaxPriority());
        Thread hiloPrioridad = new Thread(subgrupo, new Tarea("Tarea Prioridad"), "Hilo-Prioridad"); //creamos otro hilo en el subgrupo
        // Intentamos ponerle prioridad máxima global
        hiloPrioridad.setPriority(Thread.MAX_PRIORITY); // 10
        System.out.println(m + "Prioridad solicitada para Hilo-Prioridad: " + Thread.MAX_PRIORITY); //dando prioridad maxima al hilo nuevo pero el grupo lo limita e invalida la orden
        System.out.println(m + "Prioridad real de Hilo-Prioridad (limitada por el grupo): " 
                + hiloPrioridad.getPriority());
        hiloPrioridad.start();
        // ====== 6. Esperar a que terminen los hilos ======
        hilo1.join();
        hilo2.join();
        hilo3.join();
        hiloPrioridad.join();
        // hiloLambda.join();
        System.out.println("\n--- Info de grupos tras terminar los hilos ---");
        System.out.println(m + "Hilos activos en grupoPadre: " + grupoPadre.activeCount());
        System.out.println(m + "Subgrupos activos en grupoPadre: " + grupoPadre.activeGroupCount());
        System.out.println("\n" + m + "Fin de main().");
    }
}
