/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Pool_de_hilos_Atomic_Solucion3;

/**
 *
 * @author miriamhernav
 */
import java.io.*;
import java.net.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ServidorChat {
   private static final int PUERTO_MHN = 5000;

    // Backpressure:
    private static final int N_HILOS_MHN = 1;     // simultáneos atendidos
    private static final int COLA_MAX_MHN = 1;   // esperando turno

    private static final AtomicInteger contadorTickets = new AtomicInteger(0);

    public static void main(String[] args) {

        ThreadPoolExecutor pool = new ThreadPoolExecutor(
                N_HILOS_MHN, N_HILOS_MHN,
                0L, TimeUnit.MILLISECONDS,
                new ArrayBlockingQueue<>(COLA_MAX_MHN),
                new ThreadPoolExecutor.AbortPolicy() // cuando está lleno -> lanza RejectedExecutionException
        );

        try (ServerSocket server_MHN = new ServerSocket(PUERTO_MHN)) {
            System.out.println("Servidor Tickets (POOL + BACKPRESSURE) en puerto " + PUERTO_MHN);
            System.out.println("Hilos=" + N_HILOS_MHN + " | ColaMax=" + COLA_MAX_MHN);

            while (true) {
                Socket cliente_MHN = server_MHN.accept();

                try {
                    pool.execute(() -> atenderCliente(cliente_MHN));
                } catch (RejectedExecutionException ex) {
                    // Backpressure: estamos saturados -> avisamos y cerramos
                    try (PrintWriter salida = new PrintWriter(cliente_MHN.getOutputStream(), true)) {
                        salida.println("SERVIDOR_OCUPADO");
                    } catch (IOException ignored) {
                    } finally {
                        try { cliente_MHN.close(); } catch (IOException ignored) {}
                    }
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            pool.shutdown();
        }
    }

    private static void atenderCliente(Socket cliente) {
        try (
                BufferedReader entrada = new BufferedReader(new InputStreamReader(cliente.getInputStream()));
                PrintWriter salida = new PrintWriter(cliente.getOutputStream(), true)
        ) {
            // Protocolo simple:
            // Cliente manda: "TICKET"
            // Servidor responde: "TICKET:<numero>" o "ERROR"

            String peticion = entrada.readLine();

            if (peticion == null) return;

            if (peticion.equalsIgnoreCase("TICKET")) {
                int ticket = contadorTickets.incrementAndGet(); // seguro en concurrencia
                salida.println("TICKET:" + ticket);
            } else {
                salida.println("ERROR: Petición inválida. Usa TICKET");
            }

        } catch (IOException ignored) {
        } finally {
            try { cliente.close(); } catch (IOException ignored) {}
        }
    }
}
