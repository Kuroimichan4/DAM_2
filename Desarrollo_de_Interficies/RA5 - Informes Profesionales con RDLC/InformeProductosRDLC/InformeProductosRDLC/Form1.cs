using InformeProductosRDLC.TiendaInformesDataSetTableAdapters;
using Microsoft.Reporting.WinForms;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace InformeProductosRDLC
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            reportViewer2.LocalReport.DataSources.Clear();

            reportViewer2.LocalReport.ReportEmbeddedResource = "InformeProductosRDLC.InformeRDLC.rdlc";

            ProductosTableAdapter adapter = new ProductosTableAdapter();
            TiendaInformesDataSet.ProductosDataTable tabla = adapter.GetData();

            ReportDataSource rds = new ReportDataSource("Productos", (DataTable)tabla);
            reportViewer2.LocalReport.DataSources.Add(rds);

            reportViewer2.RefreshReport();
        }
    }
}
