using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MisComponentesLib
{
    public partial class RelojDigital: UserControl
    {
        // inicio las variables para la alarma y demás
        private string horaAlarma = "";
        private bool hayAlarma = false;

        private bool mostrarSegundos = true;
        private string formatoHora = "HH:mm:ss";
        private Color colorTexto = Color.Blue;
        private Color colorNormal = Color.Blue;
        private Color colorAlarma = Color.Red;
        private float tamanyoFuente = 25f;


        private string horaActual = "";


        public bool MostrarSegundos // esto es una propiedad pública. Estas actúan como una especie de guardián de una variable privada
        {
            get { return mostrarSegundos; } // get muestra el valor actual 
            set
            {
                mostrarSegundos = value;
                // value es simplemente una variable temporal que va a variar dependiendo en ese momento de lo que se a mostrarSegundos
                formatoHora = mostrarSegundos ? "HH:mm:ss" : "HH:mm"; // ternario para cuando esté en false pase a true y viceversa
            }
        }

        public string FormatoHora
        {    //esto es para se pueda leer al hacer get el formato
            get { return formatoHora; }
            // y el set es para que se pueda cambiar el formato
            set { formatoHora = value; }
        }

        public Color ColorTexto
        {
            get { return colorTexto; }
            set { colorTexto = value; }
        }

        public string HoraAlarma
        {
            get { return horaAlarma; }
            set
            {
                horaAlarma = value;
                hayAlarma = true;
            }
        }

        public float TamanyoFuente
        {
            get { return tamanyoFuente; }
            set
            {
                tamanyoFuente = value;
                this.Invalidate(); // para que se redibuje
            }
        }


        public event EventHandler EventAlarmaActivada;


        public RelojDigital()
        {
            InitializeComponent();
            colorTexto = colorNormal;
            Iniciar();
            
        }

        public void PonerAlarma(string hora)
        {
            horaAlarma = hora; 
            hayAlarma = true;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            horaActual = DateTime.Now.ToString(formatoHora);// La hora actual
            this.Invalidate(); // le dice que se vuelva a dibujar

            if (hayAlarma)
            {
                string ahora = DateTime.Now.ToString("HH:mm");

                if (ahora == horaAlarma) // comparo la hora actual con la hora de la alarma
                {
                    hayAlarma = false; // para que no salga mil veces durante el minuto que sea la alarma
                    colorTexto = colorAlarma;   // cambia el color para la alarma
                    this.Invalidate();
                    EventAlarmaActivada?.Invoke(this, EventArgs.Empty);
                    // Invoke dispara el evento
                    // en forms cuando se lanza un evento x convención se envían 2 cosas quien lo envía y la información adicional
                    // this: quien lo envía que es en este caso RelojDigital
                    // EventArgs.Empty: es xq no hay info adicional
                }
            } 
        }

        public void Iniciar() // se inicia al runear pero igual podría ponerle un botón
        {
            timer1.Enabled = true;
        }

        public void Detener()
        {
            timer1.Enabled = false;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);

            using (Brush pincel = new SolidBrush(colorTexto))
            using (Font fuente = new Font(this.Font.FontFamily, tamanyoFuente))
            {
                e.Graphics.DrawString(
                    horaActual,
                    fuente,
                    pincel,
                    new PointF(10, 10)
                );
            }
        }



    }
}
