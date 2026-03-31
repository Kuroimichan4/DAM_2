/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Synchronized;

/**
 *
 * @author Lucifer
 */
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;



public class Servidor_Synchronized {
    
    
    private static int contadorTickets = 0;
    private static final int PUERTO = 5000;

    public static void main(String[] args) {
        try (ServerSocket servidor_MHN = new ServerSocket(PUERTO)) {
            System.out.println("Servidor de tickets con synchronized en puerto " + PUERTO);

            while (true) {
                Socket cliente_MHN = servidor_MHN.accept();
                System.out.println("Cliente conectado: " + cliente_MHN.getInetAddress());

                Thread hilo_MHN = new Thread(() -> atenderCliente(cliente_MHN));
                hilo_MHN.start();
            }

        } catch (IOException e) {
            System.out.println("Error en el servidor: " + e.getMessage());
        }
    }

    private static void atenderCliente(Socket cliente) {
        try (
            BufferedReader entrada_MHN = new BufferedReader(
                new InputStreamReader(cliente.getInputStream()));
            PrintWriter salida_MHN = new PrintWriter(cliente.getOutputStream(), true)
        ) {
            String peticion_MHN = entrada_MHN.readLine();

            if (peticion_MHN != null && peticion_MHN.equalsIgnoreCase("TICKET")) {
                int ticket_MHN = generarTicket();
                salida_MHN.println("TICKET:" + ticket_MHN);
                System.out.println("Ticket enviado al cliente: " + ticket_MHN);
            } else {
                salida_MHN.println("ERROR: petición inválida. Usa TICKET");
            }

        } catch (IOException e) {
            System.out.println("Error con un cliente: " + e.getMessage());
        } finally {
            try {
                cliente.close();
            } catch (IOException e) {
                System.out.println("No se pudo cerrar el socket del cliente.");
            }
        }
    }

    private static synchronized int generarTicket() {
        contadorTickets++;
        return contadorTickets;
    }
}
