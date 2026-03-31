/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Apache_VS_Nginx;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Servidor_Apache {
    private static final int PUERTO = 5000;

    public static void main(String[] args) {
        try (ServerSocket servidor = new ServerSocket(PUERTO)) {
            System.out.println("Servidor estilo Apache en puerto " + PUERTO);

            while (true) {
                Socket cliente = servidor.accept();
                System.out.println("Nueva conexión: " + cliente.getInetAddress());

                new Thread(() -> atenderCliente(cliente)).start();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void atenderCliente(Socket cliente) {
        try (
            BufferedReader entrada = new BufferedReader(
                    new InputStreamReader(cliente.getInputStream()));
            PrintWriter salida = new PrintWriter(
                    cliente.getOutputStream(), true)
        ) {
            String mensaje = entrada.readLine();

            System.out.println("Hilo " + Thread.currentThread().getName()
                    + " atiende a " + cliente.getInetAddress()
                    + " -> " + mensaje);

            // Simulamos trabajo
            Thread.sleep(1000);

            salida.println("Respuesta Apache");

        } catch (Exception e) {
            System.out.println("Error atendiendo cliente");
        } finally {
            try {
                cliente.close();
            } catch (Exception ignored) {
            }
        }
    }
}
