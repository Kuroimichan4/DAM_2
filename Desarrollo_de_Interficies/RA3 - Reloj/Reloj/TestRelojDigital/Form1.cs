using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TestRelojDigital
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e) // esto para el botón de la alarma
        {

            relojDigital1.PonerAlarma(
                DateTime.Now.AddMinutes(1).ToString("HH:mm")
            );

            // cuando salte el evento de la alarma del RelojDigital le dice que ejecute el método de abajo
            relojDigital1.EventAlarmaActivada += RelojDigital1_AlarmaActivada;

        }
        private void RelojDigital1_AlarmaActivada(object sender, EventArgs e)
        {
            MessageBox.Show("⏰ ¡Alarma!", "TestRelojDigital");
        }



    }
}
