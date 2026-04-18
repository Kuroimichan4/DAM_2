// Si se cierra la vista diseño de nuevo es shift F para abrirla otra vez

using System.Globalization; // esto importa el espacio de nombre (formato de números, fechas, ACENTOS Y LETRAS EN ESP...)

namespace CalcIvaWinForms // nombre del paquete donde está el formulario de la calculadora
{
    public partial class ivaCalculator : Form //aquí le doy nombre a la clase y le digo de donde hereda
        // se pone partial class porque parte de la clase está en el diseño y otra aquí
    {
        // Cultura (parece que en C# se le llama así cuando se define una serie de reglas de formato) para formatear en es-ES (€ y la coma decimal)
        private readonly CultureInfo _es = CultureInfo.GetCultureInfo("es-ES"); // y readonly se usa para declarar un campo o variable que puede ser asignado solo una vez, es decir una constante

        public ivaCalculator()
        {
            InitializeComponent(); // constructor del formulario que se ha creado al crear la parte de diseño
            // y crea a continuación todos los componentes rollo botones, textboxes y demás
        }

        // estos métodos se crean solos al darle doble click al componente que sea cada uno
        private void rbIva10_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void rbD0_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void ivaCalculator_Load(object sender, EventArgs e)
        {

        }

        private void Price_Click(object sender, EventArgs e)
        {

        }

        private void labelConIva_Click(object sender, EventArgs e)
        {

        }

        private void rbIva21_CheckedChanged(object sender, EventArgs e)
        {

        }
        /// <summary>
        /// Calcula el importe total de la compra a partir del precio y la cantidad introducidos,
        /// aplicando primero el descuento seleccionado y después el IVA.
        /// Muestra el resultado sin IVA y con IVA en los cuadros de texto
        /// </summary>
        /// <param name="sender">Control/botón que ha provocado el evento, en este caso el botón Calculate</param>
        /// <param name="e">Datos asociados al evento Click</param>
 
        private void btnCalculate_Click(object sender, EventArgs e) //doble click para generar el método del boton calculate en la vista

        {
            // VALIDACIONES para el precio y ka cantidad
            if (!ParsePrecioDecimal(txtPrice, "Precio", min: 0m, out decimal precio)) return; // campo del precio/ nom del campo para los mensajes de error/el num min/ y lo que devuelve. Se pone el m para indicar que es decimal
            if (!ParseInt(txtQuantity, "Cantidad", min: 1, out int cantidad)) return;

            // Precio sin IVa
            decimal subtotal = precio * cantidad;

            // DESCUENTO, luego IVA
            decimal descuento = GetDescuentos(); // 0,05 / 0,10 / 0,20 * 0,30 si es Partner
            decimal baseSinIva = subtotal * (1 - descuento);

            decimal iva = GetIva();           // 0 / 0,04 / 0,10 / 0,21
            decimal totalConIva = baseSinIva * (1 + iva);

            // Resultados formateados en es-ES para que salga el símbolo de moneda €. Es obligatorio pasarlo a string porque si no no se puede poner en el textbox
            txtNoIva.Text = baseSinIva.ToString("C", _es); //la C es para que salga el símbolo de moneda, la C viene de Currency que es moneda en inglés
            txtWithIva.Text = totalConIva.ToString("C", _es);

        }

        /// <summary>
        /// Gestiona el cambio de estado de la opción Partner.
        /// Cuando está activada, deshabilita los descuentos manuales y aplica un descuento fijo del 30%
        /// </summary>
        /// <param name="sender">Control/botón que ha provocado el evento</param>
        /// <param name="e">Datos asociados al evento CheckedChanged</param>
        private void chkPartner_CheckedChanged(object sender, EventArgs e)
        {
// para hacer la función del check partner de forma auto, seleccionar el chkpartner darla al rayo en la pestaña de Eventos y escribir el nombre de la función que queramos y pulsar Enter

            bool hayPartner = chkPartner.Checked;

            // Si hay partner, el grupo de descuentos manuales NO aplica
            grpDiscount.Enabled = !hayPartner;

            // Opcional: dejar visible 0% cuando hay partner (el 30% se aplica por código)
            if (hayPartner)
                rbD0.Checked = true;

            // Opcional: recalcular automáticamente al marcar/desmarcar
            // btnCalculate.PerformClick();
        }

        /// <summary>
        /// Validación de números decimales y no negativos para el precio
        /// y que no sea inferior al valor mínimo indicado.
        /// </summary>
        /// <param name="tbox">Cuadro de texto del que se obtiene el valor introducido por el usuario.</param>
        /// <param name="fieldName">Nombre del campo que se utilizará en los mensajes de error.</param>
        /// <param name="min">Valor mínimo permitido para el campo.</param>
        /// <param name="value">Valor decimal obtenido del cuadro de texto si la validación es correcta.</param>
        /// <returns>Devuelve true/false si el valor es válidoo no</returns>
        private bool ParsePrecioDecimal(TextBox tbox, string fieldName, decimal min, out decimal value)
        {
            if (!decimal.TryParse(tbox.Text, NumberStyles.Number, _es, out value))
            {
                MessageBox.Show($"Introduce un valor numérico válido para '{fieldName}'.",
                                "Dato inválido", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                tbox.Focus(); tbox.SelectAll();
                return false;
            }
            if (value < min)
            { //el fieldname sale delos parámetros que este sale a su vez de el textbox del precio
                MessageBox.Show($"'{fieldName}' no puede ser menor que {min}.",
                                "Dato inválido", MessageBoxButtons.OK, MessageBoxIcon.Warning); //mesagebox es un cuadro de diálogo que muestra mensajes al usuario,
                                                                                                //mesageboxbuttons.ok es para que salga el botón de aceptar
                                                                                                //y mesageboxicon.warning es para que salga el icono de advertencia
                tbox.Focus(); tbox.SelectAll();
                return false;
            }
            return true;
        }

        // validación de numeros enteros y no negativos para la cantidad

        /// <summary>
        /// Valida que el valor introducido en un cuadro de texto sea un número entero, no negativo
        /// y que no sea inferior al valor mínimo permitido.
        /// </summary>
        /// <param name="tbox">Cuadro de texto/input en el que el usuario introduce el valor.</param>
        /// <param name="fieldName">Nombre del campo que aparecerá en los mensajes de error.</param>
        /// <param name="min">Valor mínimo permitido para el campo.</param>
        /// <param name="value">Valor entero obtenido del input que ha sido parseado a int.</param>
        /// <returns>Devuelve true/false según si el valor es válido o no.</returns>
        private bool ParseInt(TextBox tbox, string fieldName, int min, out int value) // al ser privada solo se puede usar dentro de este form
            //textBox input donde ha escrito el usuario
            //fieldName va a ser el campo dende saldrán los mensajes de error
            // el min lo paso por parámetro
            // el out value es para indicar que se va a devolver un valor por ese parámetro 

        {
            if (!int.TryParse(tbox.Text, NumberStyles.Integer, _es, out value))
            //NumberStyles.Integer, le dice que si es un int...
            //_es, con formato de los numeros españoles, devuelva este valor

            {
                MessageBox.Show($"Introduce un entero válido para '{fieldName}'.",
                                "Dato inválido", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                tbox.Focus(); 
                // Focus es para que el cursor vuelva a ese textbox, así que te muestra el mensaje de error y cuando lo cierran,
                // directamente te pone en el error que se ha escrito
                tbox.SelectAll(); //para seleccionar todo lo q  ue hay en el textbox y sustituirlo
                return false;
            }
            if (value < min) 
            {
                // metodo para mostrar errores
                MessageBox.Show($"'{fieldName}' debe ser como mínimo {min}.",
                                "Dato inválido", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                tbox.Focus(); // pone cursor en el textbox que está erroneo
                tbox.SelectAll();  // esto selecciona todo el texto del textbox para que se pueda borrar y escribir de nuevo
                return false;
            }
            return true;
        }

        /// <summary>
        /// Obtiene el porcentaje de IVA seleccionado en el formulario.
        /// </summary>
        /// <returns>
        /// Devuelve el porcentaje de IVA como valor decimal.
        /// Por ejemplo: 0.21 para el 21%, 0.10 para el 10%, 0.04 para el 4% y 0.00 para el 0%.
        /// </returns>
        private decimal GetIva()
        {
            // pilla los checkbox de los iva y dependiendo del seleccionado le da un % del iva
            if (rbIva21.Checked) return 0.21m;
            if (rbIva10.Checked) return 0.10m;
            if (rbIva4.Checked) return 0.04m;
            // rbIva0.Checked por defecto será 0 
            return 0.00m;
        }

        /// <summary>
        /// Obtiene el porcentaje de descuento aplicable según la opción seleccionada.
        /// Si la opción Partner está activada, se aplica un descuento fijo del 30%.
        /// </summary>
        /// <returns>
        /// Devuelve el descuento como valor decimal.
        /// Por ejemplo: 0.30 para el 30%, 0.20 para el 20%, 0.10 para el 10%, 0.05 para el 5% y 0.00 para el 0%.
        /// </returns>
        private decimal GetDescuentos()
        {
            // Si hay partner, 30% fijo
            if (chkPartner.Checked) return 0.30m;

            // lo mismo que con los check del iva, los pilla y llles asigna el descuento
            if (rbD20.Checked) return 0.20m;
            if (rbD10.Checked) return 0.10m;
            if (rbD5.Checked) return 0.05m;
            // rbD0.Checked por defecto
            return 0.00m;
        }
    }
}
