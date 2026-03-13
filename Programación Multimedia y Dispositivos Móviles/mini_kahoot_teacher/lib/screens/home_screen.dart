import 'package:flutter/material.dart';
import 'teacher_screen.dart';
import 'player_screen.dart';

class HomeScreen extends StatelessWidget { // esto quiere decir que la clase HomeScreen es un widget que no cambiará su apariencia
  const HomeScreen({super.key}); // el constructor del widget. El key es un identificador único para cada widget

  @override
  Widget build(BuildContext context) { //el método build le indica Como se dibujará la pantalla
    return Scaffold( // es el esqueleto de la pantalla. Proporciona una estructura básica para la aplicación, como la barra de navegación, el cuerpo...
      appBar: AppBar(title: const Text('Mini Kahoot')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center, // estp ermite centrar los hijos de la columna verticalmente
          children: [
            ElevatedButton( // Es el botón estándar de Flutter con relieve
              child: const Text('Profesor'),
              onPressed: () { // es como el onClick de js
                Navigator.push( // pone una pantalla encima de la actual
                  context,
                  MaterialPageRoute( // es una ruta que se muestra como una página completa. Da una transición de deslizamiento al navegar a la nueva pantalla.
                    builder: (_) => const TeacherScreen(), // el builder es una función que devuelve el widget que se va a mostrar en la nueva pantalla, en este caso TeacherScreen
                  ),
                );
              },
            ),
            const SizedBox(height: 20), //Es un separador invisible. Een este caso entre 2 botones
            ElevatedButton(
              child: const Text('Jugador'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const PlayerScreen(),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}