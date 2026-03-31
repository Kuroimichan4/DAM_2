/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package Java;

/**
 *
 * @author MiriamHernandezNavar
 */
import java.io.*;
import java.net.*;

public class ServidorServicio {
    public static void main(String[] args) {
        int puerto = 6000;

        try (ServerSocket servidor = new ServerSocket(puerto)) {
            System.out.println("Servicio Java iniciado en puerto " + puerto);

            while (true) {
                Socket cliente = servidor.accept();
                System.out.println("Cliente conectado: " + cliente.getInetAddress());

                BufferedReader entrada = new BufferedReader(
                        new InputStreamReader(cliente.getInputStream()));
                PrintWriter salida = new PrintWriter(cliente.getOutputStream(), true);

                String mensaje = entrada.readLine();
                System.out.println("Petición recibida: " + mensaje);

                if (mensaje != null && mensaje.equalsIgnoreCase("ESTADO")) {
                    salida.println("SERVICIO OPERATIVO");
                } else {
                    salida.println("PETICION DESCONOCIDA");
                }

                cliente.close();
            }

        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
