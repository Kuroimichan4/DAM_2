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

public class ClienteChat {
     public static void main(String[] args) {

        try (Socket socket = new Socket("localhost", 5000)) {

            BufferedReader entrada_MHN = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter salida_MHN = new PrintWriter(socket.getOutputStream(), true);

            salida_MHN.println("TICKET");

            String respuesta_MHN = entrada_MHN.readLine();
            System.out.println("Respuesta servidor: " + respuesta_MHN);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
