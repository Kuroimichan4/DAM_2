import 'package:flutter/material.dart';
import '../services/firebase_service.dart';

class AddQuestionScreen extends StatefulWidget {
  const AddQuestionScreen({super.key});

  @override
  State<AddQuestionScreen> createState() => _AddQuestionScreenState();
}

class _AddQuestionScreenState extends State<AddQuestionScreen> {
  final questionController = TextEditingController();
  final option1Controller = TextEditingController();
  final option2Controller = TextEditingController();
  final option3Controller = TextEditingController();
  final option4Controller = TextEditingController();

  int correctIndex = 0;

  Future<void> saveQuestion() async {
    final question = questionController.text.trim();
    final option1 = option1Controller.text.trim();
    final option2 = option2Controller.text.trim();
    final option3 = option3Controller.text.trim();
    final option4 = option4Controller.text.trim();

    if (question.isEmpty ||
        option1.isEmpty ||
        option2.isEmpty ||
        option3.isEmpty ||
        option4.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar( // ScaffoldMessenger es una clase que permite mostrar mensajes temporales en la pantalla, como toasts 
        const SnackBar(content: Text('Rellena todos los campos')), 
      );
      return;
    }

    await FirebaseService.addQuestionToBank(
      text: question,
      options: [option1, option2, option3, option4],
      correctIndex: correctIndex,
    );

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Pregunta guardada en Firebase')),
    );

    questionController.clear();
    option1Controller.clear();
    option2Controller.clear();
    option3Controller.clear();
    option4Controller.clear();

    setState(() {
      correctIndex = 0;
    });
  }

  @override
  void dispose() {
    questionController.dispose();
    option1Controller.dispose();
    option2Controller.dispose();
    option3Controller.dispose();
    option4Controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crear pregunta'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: questionController,
              decoration: const InputDecoration(labelText: 'Pregunta'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: option1Controller,
              decoration: const InputDecoration(labelText: 'Opción 1'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: option2Controller,
              decoration: const InputDecoration(labelText: 'Opción 2'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: option3Controller,
              decoration: const InputDecoration(labelText: 'Opción 3'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: option4Controller,
              decoration: const InputDecoration(labelText: 'Opción 4'),
            ),
            const SizedBox(height: 20),
            DropdownButtonFormField<int>(
              value: correctIndex,
              decoration: const InputDecoration(
                labelText: 'Respuesta correcta',
              ),
              items: const [
                DropdownMenuItem(value: 0, child: Text('Opción 1')),
                DropdownMenuItem(value: 1, child: Text('Opción 2')),
                DropdownMenuItem(value: 2, child: Text('Opción 3')),
                DropdownMenuItem(value: 3, child: Text('Opción 4')),
              ],
              onChanged: (value) {
                setState(() {
                  correctIndex = value!;
                });
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: saveQuestion,
              child: const Text('Guardar pregunta'),
            ),
          ],
        ),
      ),
    );
  }
}