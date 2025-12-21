using System;

class Program
{
    static void Main()
    {
        // aquí va tu programa
        Console.WriteLine("Menu de la calculadora");

        bool continuar = true;
        while (continuar)
        {
            Console.WriteLine("Seleccione una operacion:");
            Console.WriteLine("1. Suma");
            Console.WriteLine("2. Resta");
            Console.WriteLine("3. Multiplicacion");
            Console.WriteLine("4. Division");
            Console.WriteLine("5. Potencia");
            Console.WriteLine("6.Raiz cuadrada");
            Console.WriteLine("7. Salir");

            string opcion = Console.ReadLine();

            switch (opcion)
            {
                case "1":
                    suma();
                    break;
                case "2":
                    resta();
                    break;
                case "3":
                    multiplicacion();
                    break;
                case "4":
                    division();
                    break;
                case "5":
                    potencia();
                    break;
                case "6":
                    raizCuadrada();
                    break;
                case "7":
                    continuar = false;
                    break;
                default:
                    Console.WriteLine("Opcion no valida, intente de nuevo.");
                    break;
            }

            Console.WriteLine();
        }

    }

    static double pedirDouble(string mensaje)
    {
        while (true)
        {
            Console.Write(mensaje);
            string? s = Console.ReadLine(); // el ? es para indicar que s puede ser null
            if (double.TryParse(s, out double v)) return v;
            // double.TryParse(...) intenta convertir el texto a double
            // out double v es una variable que se crea en el momento para guardar el resultado
            // si la conversion es exitosa, TryParse devuelve true y v tiene el valor convertido
            Console.WriteLine("Entrada inválida. Escribe un número.");
        }
    }

    static void suma() // static double Suma(double a, double b) => a + b;
    {
        Console.WriteLine("Ingrese dos numeros:");
        double a = pedirDouble("Ingrese el primer numero: ");
        double b = pedirDouble("Ingrese el segundo numero: ");
        double resultado = a + b;
        Console.WriteLine($"El resultado de la suma es: {resultado}");

    }

    static void resta()
    {
        Console.WriteLine("Ingrese dos numeros:");
        double a = pedirDouble("Ingrese el primer numero: ");
        double b = pedirDouble("Ingrese el segundo numero: ");
        double resultado = a - b;
        Console.WriteLine($"El resultado de la resta es: {resultado}");
    }

    static void multiplicacion()
    {
        Console.WriteLine("Ingrese dos numeros:");
        double a = pedirDouble("Ingrese el primer numero: ");
        double b = pedirDouble("Ingrese el segundo numero: ");
        double resultado = a * b;
        Console.WriteLine($"El resultado de la multiplicacion es: {resultado}");
    }

    static void division()
    {
        Console.WriteLine("Ingrese dos numeros:");
        double a = pedirDouble();
        double b;
        while (true)
        {
            b = pedirDouble("Ingrese el segundo numero (no puede ser cero): ");
            if (b != 0) break;
            Console.WriteLine("El segundo numero no puede ser cero. Intente de nuevo.");
        }
        double resultado = a / b;
        Console.WriteLine($"El resultado de la division es: {resultado}");
    }
    static void potencia()
    {
        Console.WriteLine("Ingrese la base y el exponente:");
        double a = pedirDouble("Ingrese la base: ");
        double b = pedirDouble("Ingrese el exponente: ");
        double resultado = Math.Pow(a, b); // Math.Pow calcula a elevado a b
        Console.WriteLine($"El resultado de la potencia es: {resultado}");
    }
    static void raizCuadrada()
    {
        double a;
        while (true)
        {
            a = pedirDouble("Ingrese un numero (no puede ser negativo): ");
            if (a >= 0) break;
            Console.WriteLine("El numero no puede ser negativo. Intente de nuevo.");
        }
        double resultado = Math.Sqrt(a); // Math.Sqrt calcula la raiz cuadrada
        Console.WriteLine($"El resultado de la raiz cuadrada es: {resultado}");
    }
}
