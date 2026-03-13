import 'package:flutter/material.dart'; // Esto importa las herramientas visuales básicas de Flutter para hacer la interfaz.
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'screens/home_screen.dart';

void main() async { // async aqui permite que el programa espere a que se complete la inicialización de Firebase antes de continuar con la ejecución de la aplicación.
  WidgetsFlutterBinding.ensureInitialized(); // Asegura que Flutter esté completamente inicializado antes de ejecutar cualquier código adicional.
  await Firebase.initializeApp( // Inicializa Firebase con la configuración específica para la plataforma actual.
    options: DefaultFirebaseOptions.currentPlatform, // Es un archivo autogenerado que carga las credenciales de las BBDD para cada plataforma. Se parece a python con un diccionario de configuración y el .env
  );
  runApp(const MyApp()); // Ejecuta la aplicación visualmente, MyApp es el widget raíz de la aplicación.
}
class MyApp extends StatelessWidget { // StatelessWidget es un widget que no tiene estado mutable, lo que significa que su apariencia no cambiará a lo largo del tiempo
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp( // Es el widget/contenedor que define el tema, título y la pantalla de inicio de la aplicación.
      title: 'Mini Kahoot',
      debugShowCheckedModeBanner: false, // Esto elimina la etiqueta de "debug" que aparece en la esquina de la aplicación cuando se ejecuta en modo de desarrollo
      theme: ThemeData.dark(),
      home: const HomeScreen(), // Define la pantalla de inicio de la aplicación, que en este caso es HomeScreen.
    );
  }
}
