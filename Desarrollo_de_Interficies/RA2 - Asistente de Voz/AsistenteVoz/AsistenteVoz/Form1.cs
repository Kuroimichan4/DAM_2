using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics; // esto es para poder interactuar con el sistema como el block de notas o el chrome con Process.start()
using System.Drawing; // cambia el color del panel
using System.Globalization; // esto es para el tema del reconoci,iento de idiomas
using System.IO;
using System.Linq;
using System.Speech.Recognition; // obvio para el reconocimiento de voz y el micro
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms; // como siempre para el forms
using System.IO; // para el dvd


namespace AsistenteVoz
{
    public partial class Form1 : Form
    {
        // estos van a ser como los atributos/campos de la clase 
        private SpeechRecognitionEngine _rec; // esto para escuchar y reconocer la voz
        private CultureInfo _culture; // esto es para que reconozca el idioma
        private const float MIN_WAKARU = 0.65f; // esto es el porcentaje de seguridad con el que entiende algo

        public Form1()
        {
            InitializeComponent();
            Shown += Form1_Shown;// esto se dispara cuando la ventana se crea y aparece para asegurarnos que ya está todo el sistema iniciadi y listo
            FormClosing += Form1_FormClosing; // para parar el reconocimiento al cerrar
            btnStart.Click += (_, __) => StartRecognition();
            btnStop.Click += (_, __) => StopRecognition();
        }
        private void Form1_Shown(object sender, EventArgs e)
        {
            // TODO: inicializar el reconocedor es-Es para español
            // esto primero define el idioma (también puedo poner es_ES directamente pero bueno...)
            _culture = new CultureInfo("es-ES");
            // y estoi ya instancia el reconocedor
            _rec = new SpeechRecognitionEngine(_culture);

            // 1. Comprobar reconocedores instalados (si hay idiomas puestos vaya)
            bool hayReconocedor = false;
            foreach (var reconizer in SpeechRecognitionEngine.InstalledRecognizers()) // InstalledRecognizers son los motores de voz instalados
            {
                if (reconizer.Culture.Equals(_culture))
                {
                    hayReconocedor = true;
                    break;
                }
            }

            if (!hayReconocedor)
            {
                Log($"ERROR: No hay reconocedor instalado para {_culture.Name}.", true);
                MessageBox.Show(
                    "No hay motor de voz para " + _culture.Name + " instalado. Prueba con en-US o instala el reconocimiento de voz de Windows.",
                    "Error de reconocimiento", 
                    MessageBoxButtons.OK, 
                    MessageBoxIcon.Warning
                    );
                return;
            }

            //--------------------------------------------------//
            // 2. Crear gram´atica de comandos
            // aquí añado las palabras o frases que queremos que reconozca en una lista de la liobrería del speech.recognition es como un array de parámetros

            // palabras sueltas Choices
            var comandos = new Choices(
                "hola",
                "limpiar",
                "salir",
                "color rojo",
                "color verde",
                "color azul",
                "abrir bloc de notas",
                "abrir navegador",
                "que tal",
                "no entiendes nada",
                "callate",
                "abrir dvd"
                );

            //--------------------------------------------------//
            // esto también lo puedo hacer así: 
            // string[] misFrases = { "hola", "adiós", "abrir" };
            // var comandos = new Choices(misFrases); 
            //--------------------------------------------------//

            //--------------------------------------------------//
            // GrammarBuilder prepara la estructura para las frases, es como el plano 
            GrammarBuilder builder = new GrammarBuilder(); // esto crea el constructor vacío (le puedo poner "comandos" directamente entre parentesis pero así tiene mas claro la gtramatica antes de añadir los "comandos")
            builder.Culture = _culture; // esto es para decirle en qué idioma está lña gramatica y que no se lie tanto ya que le estoy poniendo esp
            builder.Append(comandos); // y aquí le añado las palabras


            // ------------- esto es por si vamos a hacer frases compuestas rollo losiguiente:  --------//
            //Choices nombresAsistente = new Choices("Asistente", "Jarvis", "Computadora");
            //Choices acciones = new Choices("abre", "cierra", "ejecuta");
            //Choices programas = new Choices("el navegador", "el bloque de notas");

            //GrammarBuilder builder = new GrammarBuilder();
            //builder.Append(nombresAsistente); // 1ª parte de la frase
            //builder.Append(acciones);         // 2ª parte de la frase
            //builder.Append(programas);        // 3ª parte de la frase

            // Ahora el motor reconocerá: "Jarvis abre el navegador"
            //--------------------------------------------------//

            // Grammar paquete final que se pasa al motor
            // aquí pasa el plano a gramática real
            Grammar grammar = new Grammar(builder);

            //--------------------------------------------------//
            // 3. Cargar la gram´atica en el motor
            // aquúi se le dice cuales son las frases a reconocer
            _rec.LoadGrammar(grammar);

            //--------------------------------------------------//
            // 4. Configurar el micr´ofono como fuente
            _rec.SetInputToDefaultAudioDevice(); // esto pilla el que tenga win por defecto

            // SpeechRecognized es un evento o un listener que reconoce cuando ha encontrado una palabra o frase válida
            // Rec_SpeechRecognized es la función que contiene las intrucciones que debe hacer al reconocer las palabras
            // al poner += se le dice que añada la la ejecución del metodo a la lista de tareas
            _rec.SpeechRecognized += Rec_SpeechRecognized;



        }
        private void StartRecognition()
        {
            // TODO: iniciar reconocimiento as´ıncrono
            try
            {
                // el async es para que vaya por otro hilo a la ventana del form y tenerlo en segundo plano y multiple para que no se pare con una sola palabra
                _rec.RecognizeAsync(RecognizeMode.Multiple);
                Log("Asistente escuchando...");
                // para evitar que le den como loco epiléptico al botón y crashee
                btnStart.Enabled = false;
                btnStop.Enabled = true;
            }
            catch (InvalidOperationException)
            {
                Log("Asistente ya iniciado");
            }
            catch (Exception ex)
            {
                Log("Error al iniciar: " + ex.Message, true);
            }
        }
        private void StopRecognition()
        {
            // TODO: parar reconocimiento
            try
            {
                _rec.RecognizeAsyncCancel(); // cancela lo que estaba haciendo si estaba en medio de algo
                _rec.RecognizeAsyncStop(); // para el reconocimiento del todo
                Log("Asistente detenido");
                btnStart.Enabled = true;
                btnStop.Enabled = false;
            }
            catch (Exception ex)
            {
                Log("Error al detener asistente: " + ex);
            }
        }
        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            try
            {
                StopRecognition();
                _rec?.Dispose();
                // liberra los recursos del audio, ram, hilos, motor iunterno y demás que se estaba usando si no está grabando
                // con el ? que es el condicional como en SQL creo que se llamaba ternario
            }
            catch (Exception ex)
            {
                Log("Error: " + ex);
            }
        }

    // Esto lo pongo porque quiero, no forma parte del ejercicio pero quiero probar XD
    private string BuscarUnidadDvd()
        {
            foreach (var drive in DriveInfo.GetDrives())
            {
                // DriveType.CDRom = lector CD/DVD
                if (drive.DriveType == DriveType.CDRom && drive.IsReady)
                    return drive.Name.TrimEnd('\\'); // Devuelve por ejemplo "D:"
            }
            return null;
        }

        private void ReproducirDvdAuto(string rutaVlcExe)
        {
            string unidad = BuscarUnidadDvd();
            if (unidad == null)
            {
                Log("No hay DVD, búscate la vida");
                return;
            }

            string urlDvd = $"dvd:///{unidad}/";

            var psi = new ProcessStartInfo
            {
                FileName = rutaVlcExe,
                Arguments = urlDvd,
                UseShellExecute = false
            };

            Process.Start(psi);
        }

    private void Rec_SpeechRecognized(object sender, SpeechRecognizedEventArgs e)
        {
            // TODO: filtrar por confianza y ejecutar acciones
            string texto = e.Result.Text; // lo que ha entendido
            float wakaru = e.Result.Confidence; // esto es la confianza con lo que entiende algo, la he puesto a un 0.65

            //Ahora como los textbox, panel, button y demás cosas del form, pueden provocar errores si vienen ordenes/eventos para ellos desde otros hilos, se tiene que usar BeginInvoke
            // BeginInvoke mete el código en el hilo original de la interfaz del Form 
            BeginInvoke(new Action(() =>
            {
                if (wakaru < MIN_WAKARU)
                {
                    Log($"No estoy seguro de haber entendido: {texto} ({wakaru:0.00})"); //  ({wakaru:0.00}) para que salga formateado el % de lo entendido
                    return;
                }

                labelTextoReconocido.Text = texto;
                Log($"Entendí: {texto} ({wakaru:0.00})");

                // ------------ Switch según lo que entienda ---------
                switch (texto)
                {
                    case "hola":
                        Log("Hola, soy tu esclavo");
                        labelRespuesta.Text = "Hola, soy tu esclavo";
                        break;

                    case "que tal":
                        Log("Mal, soy tu esclavo ¿recuerdas?");
                        labelRespuesta.Text = "Mal, soy tu esclavo ¿recuerdas?";
                        break;

                    case "callate":
                        Log("¡Oblígame!");
                        labelRespuesta.Text = "¡Oblígame!";
                        try
                        {
                            string urlImagen = "https://ih1.redbubble.net/image.701600143.8934/raf,360x360,075,t,fafafa:ca443f4786.u1.jpg";

                            Process.Start(new ProcessStartInfo
                            {
                                FileName = urlImagen,
                                UseShellExecute = true 
                            });
                        }
                        catch (Exception ex)
                        {
                            Log("No se pudo abrir la imagen: " + ex.Message, true);
                        }
                        break;

                    case "no entiendes nada":
                        Log("Si quieres que trabaje mejor, págame");
                        labelRespuesta.Text = "Si quieres que trabaje mejor, págame";
                        break;

                    case "limpiar":
                        textLog.Clear();
                        labelRespuesta.Text = "";
                        break;

                    case "salir":
                        Close();
                        break;

                    case "color rojo":
                        panelColor.BackColor = Color.Red;
                        labelRespuesta.Text = "";
                        break;

                    case "color verde":
                        panelColor.BackColor = Color.SeaGreen;
                        labelRespuesta.Text = "";
                        break;

                    case "color azul":
                        panelColor.BackColor = Color.Blue;
                        labelRespuesta.Text = "";
                        break;

                    case "abrir bloc de notas":
                        Process.Start("notepad.exe");
                        labelRespuesta.Text = "";
                        // process es una clase de .NET para lanzar procesos del sistema operativo
                        // no hace falta poner la ruta xq windows la tiene en el path del sistema
                        break;

                    case "abrir navegador":
                        Process.Start(new ProcessStartInfo("https://www.google.com")
                        // el processstarinfo es para decirle como debe de abrir lo que queremos
                        {
                            UseShellExecute = true
                            // esto es para decirle que no lo tiene que abrir como exe, sino que lo interprete el shell de windows y lo abra como debe
                        });
                        labelRespuesta.Text = "";
                        break;

                    case "abrir dvd":
                        ReproducirDvdAuto(@"C:\Program Files\VideoLAN\VLC\vlc.exe");
                        labelRespuesta.Text = "";
                        break;
                }

            }));

        }
        private void Log(string msg, bool isError = false) // esto es para el formateo de los mensajes y los saltos de linea le añado la \r porque no me hace llos saltos bien
        {
            textLog.AppendText($"[{DateTime.Now:HH:mm:ss}] {msg}\r\n");
        }

        // También se puede hacer así para que reconozca el sistema operativo en el que está y se adapte al sistema para hacer el salto
        //private void Log(string msg)
        //{
        //    textLog.AppendText(
        //        "[" + DateTime.Now.ToString("HH:mm:ss") + "] " + msg + Environment.NewLine
        //    );
        //}



    }

}

