using Microsoft.Reporting.WinForms;

namespace InformeProductosRDLC
{
    partial class Form1
    {
        /// <summary>
        /// Variable del diseñador necesaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Limpiar los recursos que se estén usando.
        /// </summary>
        /// <param name="disposing">true si los recursos administrados se deben desechar; false en caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Código generado por el Diseñador de Windows Forms

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InitializeComponent()
        {
            this.tiendaInformesDataSet1 = new InformeProductosRDLC.TiendaInformesDataSet();
            this.tiendaInformesDataSet2 = new InformeProductosRDLC.TiendaInformesDataSet();
            this.reportViewer2 = new Microsoft.Reporting.WinForms.ReportViewer();
            ((System.ComponentModel.ISupportInitialize)(this.tiendaInformesDataSet1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.tiendaInformesDataSet2)).BeginInit();
            this.SuspendLayout();
            // 
            // tiendaInformesDataSet1
            // 
            this.tiendaInformesDataSet1.DataSetName = "TiendaInformesDataSet";
            this.tiendaInformesDataSet1.SchemaSerializationMode = System.Data.SchemaSerializationMode.IncludeSchema;
            // 
            // tiendaInformesDataSet2
            // 
            this.tiendaInformesDataSet2.DataSetName = "TiendaInformesDataSet";
            this.tiendaInformesDataSet2.SchemaSerializationMode = System.Data.SchemaSerializationMode.IncludeSchema;
            // 
            // reportViewer2
            // 
            this.reportViewer2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.reportViewer2.LocalReport.ReportEmbeddedResource = "InformeProductosRDLC.InformeRDLC.rdlc";
            this.reportViewer2.Name = "ReportViewer";
            this.reportViewer2.TabIndex = 0;
            // 
            // Form1
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.Controls.Add(this.reportViewer2);
            ((System.ComponentModel.ISupportInitialize)(this.tiendaInformesDataSet1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.tiendaInformesDataSet2)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private TiendaInformesDataSet tiendaInformesDataSet1;
        private TiendaInformesDataSet tiendaInformesDataSet2;
        private ReportViewer reportViewer2;
    }
}

