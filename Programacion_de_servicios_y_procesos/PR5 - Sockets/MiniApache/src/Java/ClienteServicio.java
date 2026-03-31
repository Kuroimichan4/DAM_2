/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Java;

/**
 *
 * @author MiriamHernandezNavar
 */
import java.io.*;
import java.net.*;

public class ClienteServicio {
    public static void main(String[] args) {
        String host = "localhost";
        int puerto = 6000;

        try (Socket socket = new Socket(host, puerto)) {
            BufferedReader entrada = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));
            PrintWriter salida = new PrintWriter(socket.getOutputStream(), true);

            salida.println("ESTADO");

            String respuesta = entrada.readLine();
            System.out.println("Respuesta del servidor: " + respuesta);

        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
