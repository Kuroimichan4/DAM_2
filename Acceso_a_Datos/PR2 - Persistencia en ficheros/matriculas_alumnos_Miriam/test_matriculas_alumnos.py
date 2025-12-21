# test_matriculas_alumnos.py
from dominio.Alumno import Alumno
from servicio.AlumnosMatriculados import AlumnosMatriculados

def menu():
    print("\n---==={ Matrículas de Alumnos }===---")
    print("1- Matricular alumno")
    print("2- Listar alumnos")
    print("3- Eliminar archivo de alumnos")
    print("4- Salir")

def main():
    while True:
        menu() #llamo al menú primero

        opcion = input("Elige opción (1-4): ").strip()

        if opcion == "1":
            nombre = input("Nombre del alumno: ").lower()
            if nombre:
                # llamamos al metodo e instanciamos un objeto alumno con el nombre del input
                AlumnosMatriculados.matricular_alumno(Alumno(nombre))
                print("Alumno matriculado")
            else:
                print("Nombre vacío")
        elif opcion == "2":
            alumnos = AlumnosMatriculados.listar_alumnos()
            if not alumnos:
                print("No hay alumnos matriculados.")
            else:
                print("Alumnos:")
                for i, nom in enumerate(alumnos, 1):  # el 1 es para indicar que empezamos desde el 1 y no del 0
                    print(f"  {i}. {nom}")
        elif opcion == "3":
            AlumnosMatriculados.eliminar_alumnos()
            print("Archivo eliminado")
        elif opcion == "4":
            print("Saliendo del programa")
            break
        else:
            print("Opción inválida. Prueba 1-4.")

if __name__ == "__main__":
    main()

