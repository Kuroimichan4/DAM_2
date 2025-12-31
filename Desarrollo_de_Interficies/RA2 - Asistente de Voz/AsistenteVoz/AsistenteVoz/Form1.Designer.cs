namespace AsistenteVoz
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
            this.btnStart = new System.Windows.Forms.Button();
            this.btnStop = new System.Windows.Forms.Button();
            this.labelTextoReconocido = new System.Windows.Forms.Label();
            this.panelColor = new System.Windows.Forms.Panel();
            this.textLog = new System.Windows.Forms.TextBox();
            this.labelRespuesta = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // btnStart
            // 
            this.btnStart.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(128)))), ((int)(((byte)(255)))), ((int)(((byte)(128)))));
            this.btnStart.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btnStart.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.btnStart.Location = new System.Drawing.Point(29, 34);
            this.btnStart.Name = "btnStart";
            this.btnStart.Size = new System.Drawing.Size(87, 23);
            this.btnStart.TabIndex = 0;
            this.btnStart.Text = "Iniciar";
            this.btnStart.UseVisualStyleBackColor = false;
            // 
            // btnStop
            // 
            this.btnStop.BackColor = System.Drawing.Color.Firebrick;
            this.btnStop.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.btnStop.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.btnStop.Location = new System.Drawing.Point(144, 34);
            this.btnStop.Name = "btnStop";
            this.btnStop.Size = new System.Drawing.Size(87, 23);
            this.btnStop.TabIndex = 1;
            this.btnStop.Text = "Stop";
            this.btnStop.UseVisualStyleBackColor = false;
            // 
            // labelTextoReconocido
            // 
            this.labelTextoReconocido.AutoSize = true;
            this.labelTextoReconocido.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.labelTextoReconocido.Font = new System.Drawing.Font("Permanent Marker", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelTextoReconocido.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.labelTextoReconocido.Location = new System.Drawing.Point(25, 255);
            this.labelTextoReconocido.Name = "labelTextoReconocido";
            this.labelTextoReconocido.Size = new System.Drawing.Size(0, 27);
            this.labelTextoReconocido.TabIndex = 2;
            this.labelTextoReconocido.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // panelColor
            // 
            this.panelColor.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.panelColor.Location = new System.Drawing.Point(29, 80);
            this.panelColor.Name = "panelColor";
            this.panelColor.Size = new System.Drawing.Size(202, 136);
            this.panelColor.TabIndex = 3;
            // 
            // textLog
            // 
            this.textLog.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.textLog.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textLog.Font = new System.Drawing.Font("Permanent Marker", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textLog.Location = new System.Drawing.Point(257, 34);
            this.textLog.Multiline = true;
            this.textLog.Name = "textLog";
            this.textLog.ReadOnly = true;
            this.textLog.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textLog.Size = new System.Drawing.Size(450, 182);
            this.textLog.TabIndex = 4;
            // 
            // labelRespuesta
            // 
            this.labelRespuesta.AutoSize = true;
            this.labelRespuesta.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.labelRespuesta.Font = new System.Drawing.Font("Permanent Marker", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelRespuesta.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.labelRespuesta.Location = new System.Drawing.Point(25, 309);
            this.labelRespuesta.Name = "labelRespuesta";
            this.labelRespuesta.Size = new System.Drawing.Size(0, 27);
            this.labelRespuesta.TabIndex = 5;
            this.labelRespuesta.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.label1.Font = new System.Drawing.Font("Permanent Marker", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label1.Location = new System.Drawing.Point(26, 239);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(41, 15);
            this.label1.TabIndex = 6;
            this.label1.Text = "Orden:";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.SystemColors.ControlDarkDark;
            this.label2.Font = new System.Drawing.Font("Permanent Marker", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label2.Location = new System.Drawing.Point(26, 294);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(62, 15);
            this.label2.TabIndex = 7;
            this.label2.Text = "Respuesta:";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Black;
            this.ClientSize = new System.Drawing.Size(738, 352);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.labelRespuesta);
            this.Controls.Add(this.textLog);
            this.Controls.Add(this.panelColor);
            this.Controls.Add(this.labelTextoReconocido);
            this.Controls.Add(this.btnStop);
            this.Controls.Add(this.btnStart);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnStart;
        private System.Windows.Forms.Button btnStop;
        private System.Windows.Forms.Label labelTextoReconocido;
        private System.Windows.Forms.Panel panelColor;
        private System.Windows.Forms.TextBox textLog;
        private System.Windows.Forms.Label labelRespuesta;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
    }
}

