namespace CalcIvaWinForms
{
    partial class ivaCalculator
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            txtPrice = new TextBox();
            txtQuantity = new TextBox();
            rbIva0 = new RadioButton();
            rbIva4 = new RadioButton();
            rbIva10 = new RadioButton();
            rbIva21 = new RadioButton();
            rbD0 = new RadioButton();
            rbD5 = new RadioButton();
            rbD10 = new RadioButton();
            rbD20 = new RadioButton();
            grpIva = new GroupBox();
            grpDiscount = new GroupBox();
            btnCalculate = new Button();
            txtNoIva = new TextBox();
            txtWithIva = new TextBox();
            Price = new Label();
            Cantidad = new Label();
            labelNoIva = new Label();
            labelConIva = new Label();
            chkPartner = new CheckBox();
            grpIva.SuspendLayout();
            grpDiscount.SuspendLayout();
            SuspendLayout();
            // 
            // txtPrice
            // 
            txtPrice.AccessibleName = "txtPrice";
            txtPrice.Location = new Point(109, 26);
            txtPrice.Name = "txtPrice";
            txtPrice.Size = new Size(167, 23);
            txtPrice.TabIndex = 0;
            // 
            // txtQuantity
            // 
            txtQuantity.AccessibleName = "txtQuantity";
            txtQuantity.Location = new Point(109, 63);
            txtQuantity.Name = "txtQuantity";
            txtQuantity.Size = new Size(167, 23);
            txtQuantity.TabIndex = 1;
            // 
            // rbIva0
            // 
            rbIva0.AccessibleName = "rbIva";
            rbIva0.AutoSize = true;
            rbIva0.Location = new Point(58, 22);
            rbIva0.Name = "rbIva0";
            rbIva0.Size = new Size(41, 19);
            rbIva0.TabIndex = 2;
            rbIva0.TabStop = true;
            rbIva0.Text = "0%";
            rbIva0.UseVisualStyleBackColor = true;
            // 
            // rbIva4
            // 
            rbIva4.AutoSize = true;
            rbIva4.Location = new Point(58, 57);
            rbIva4.Name = "rbIva4";
            rbIva4.Size = new Size(41, 19);
            rbIva4.TabIndex = 3;
            rbIva4.TabStop = true;
            rbIva4.Text = "4%";
            rbIva4.UseVisualStyleBackColor = true;
            // 
            // rbIva10
            // 
            rbIva10.AutoSize = true;
            rbIva10.Location = new Point(58, 92);
            rbIva10.Name = "rbIva10";
            rbIva10.Size = new Size(47, 19);
            rbIva10.TabIndex = 4;
            rbIva10.TabStop = true;
            rbIva10.Text = "10%";
            rbIva10.UseVisualStyleBackColor = true;
            rbIva10.CheckedChanged += rbIva10_CheckedChanged;
            // 
            // rbIva21
            // 
            rbIva21.AutoSize = true;
            rbIva21.Location = new Point(58, 127);
            rbIva21.Name = "rbIva21";
            rbIva21.Size = new Size(47, 19);
            rbIva21.TabIndex = 5;
            rbIva21.TabStop = true;
            rbIva21.Text = "21%";
            rbIva21.UseVisualStyleBackColor = true;
            rbIva21.CheckedChanged += rbIva21_CheckedChanged;
            // 
            // rbD0
            // 
            rbD0.AutoSize = true;
            rbD0.Location = new Point(54, 22);
            rbD0.Name = "rbD0";
            rbD0.Size = new Size(41, 19);
            rbD0.TabIndex = 6;
            rbD0.TabStop = true;
            rbD0.Text = "0%";
            rbD0.UseVisualStyleBackColor = true;
            rbD0.CheckedChanged += rbD0_CheckedChanged;
            // 
            // rbD5
            // 
            rbD5.AutoSize = true;
            rbD5.Location = new Point(54, 57);
            rbD5.Name = "rbD5";
            rbD5.Size = new Size(41, 19);
            rbD5.TabIndex = 7;
            rbD5.TabStop = true;
            rbD5.Text = "5%";
            rbD5.UseVisualStyleBackColor = true;
            // 
            // rbD10
            // 
            rbD10.AutoSize = true;
            rbD10.Location = new Point(54, 92);
            rbD10.Name = "rbD10";
            rbD10.Size = new Size(47, 19);
            rbD10.TabIndex = 8;
            rbD10.TabStop = true;
            rbD10.Text = "10%";
            rbD10.UseVisualStyleBackColor = true;
            // 
            // rbD20
            // 
            rbD20.AutoSize = true;
            rbD20.Location = new Point(54, 127);
            rbD20.Name = "rbD20";
            rbD20.Size = new Size(47, 19);
            rbD20.TabIndex = 9;
            rbD20.TabStop = true;
            rbD20.Text = "20%";
            rbD20.UseVisualStyleBackColor = true;
            // 
            // grpIva
            // 
            grpIva.Controls.Add(rbIva0);
            grpIva.Controls.Add(rbIva4);
            grpIva.Controls.Add(rbIva10);
            grpIva.Controls.Add(rbIva21);
            grpIva.Location = new Point(34, 132);
            grpIva.Name = "grpIva";
            grpIva.Size = new Size(242, 161);
            grpIva.TabIndex = 10;
            grpIva.TabStop = false;
            grpIva.Text = "Tipo de Iva";
            // 
            // grpDiscount
            // 
            grpDiscount.Controls.Add(rbD0);
            grpDiscount.Controls.Add(rbD5);
            grpDiscount.Controls.Add(rbD20);
            grpDiscount.Controls.Add(rbD10);
            grpDiscount.Location = new Point(317, 132);
            grpDiscount.Name = "grpDiscount";
            grpDiscount.Size = new Size(255, 161);
            grpDiscount.TabIndex = 11;
            grpDiscount.TabStop = false;
            grpDiscount.Text = "Tipo de Descuento";
            // 
            // btnCalculate
            // 
            btnCalculate.Location = new Point(224, 347);
            btnCalculate.Name = "btnCalculate";
            btnCalculate.Size = new Size(142, 57);
            btnCalculate.TabIndex = 13;
            btnCalculate.Text = "Calculate";
            btnCalculate.UseVisualStyleBackColor = true;
            btnCalculate.Click += btnCalculate_Click;
            // 
            // txtNoIva
            // 
            txtNoIva.Location = new Point(394, 63);
            txtNoIva.Name = "txtNoIva";
            txtNoIva.Size = new Size(178, 23);
            txtNoIva.TabIndex = 14;
            // 
            // txtWithIva
            // 
            txtWithIva.Location = new Point(394, 26);
            txtWithIva.Name = "txtWithIva";
            txtWithIva.Size = new Size(178, 23);
            txtWithIva.TabIndex = 15;
            txtWithIva.TextChanged += textBox2_TextChanged;
            // 
            // Price
            // 
            Price.AutoSize = true;
            Price.Location = new Point(34, 29);
            Price.Name = "Price";
            Price.Size = new Size(33, 15);
            Price.TabIndex = 16;
            Price.Text = "Price";
            Price.Click += Price_Click;
            // 
            // Cantidad
            // 
            Cantidad.AutoSize = true;
            Cantidad.Location = new Point(24, 63);
            Cantidad.Name = "Cantidad";
            Cantidad.Size = new Size(55, 15);
            Cantidad.TabIndex = 17;
            Cantidad.Text = "Cantidad";
            // 
            // labelNoIva
            // 
            labelNoIva.AutoSize = true;
            labelNoIva.Location = new Point(317, 66);
            labelNoIva.Name = "labelNoIva";
            labelNoIva.Size = new Size(43, 15);
            labelNoIva.TabIndex = 18;
            labelNoIva.Text = "Sin IVA";
            // 
            // labelConIva
            // 
            labelConIva.AutoSize = true;
            labelConIva.Location = new Point(317, 29);
            labelConIva.Name = "labelConIva";
            labelConIva.Size = new Size(49, 15);
            labelConIva.TabIndex = 19;
            labelConIva.Text = "Con IVA";
            labelConIva.Click += labelConIva_Click;
            // 
            // chkPartner
            // 
            chkPartner.AutoSize = true;
            chkPartner.Location = new Point(39, 314);
            chkPartner.Name = "chkPartner";
            chkPartner.Size = new Size(109, 19);
            chkPartner.TabIndex = 20;
            chkPartner.Text = "Partner 30% fijo";
            chkPartner.UseVisualStyleBackColor = true;
            chkPartner.CheckedChanged += chkPartner_CheckedChanged;
            // 
            // ivaCalculator
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ActiveBorder;
            ClientSize = new Size(623, 450);
            Controls.Add(chkPartner);
            Controls.Add(labelConIva);
            Controls.Add(labelNoIva);
            Controls.Add(Cantidad);
            Controls.Add(grpDiscount);
            Controls.Add(Price);
            Controls.Add(txtWithIva);
            Controls.Add(txtNoIva);
            Controls.Add(btnCalculate);
            Controls.Add(grpIva);
            Controls.Add(txtQuantity);
            Controls.Add(txtPrice);
            Name = "ivaCalculator";
            Text = "IVA Calculator";
            Load += ivaCalculator_Load;
            grpIva.ResumeLayout(false);
            grpIva.PerformLayout();
            grpDiscount.ResumeLayout(false);
            grpDiscount.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtPrice;
        private TextBox txtQuantity;
        private RadioButton rbIva0;
        private RadioButton rbIva4;
        private RadioButton rbIva10;
        private RadioButton rbIva21;
        private RadioButton rbD0;
        private RadioButton rbD5;
        private RadioButton rbD10;
        private RadioButton rbD20;
        private GroupBox grpIva;
        private GroupBox grpDiscount;
        private Button btnCalculate;
        private TextBox txtNoIva;
        private TextBox txtWithIva;
        private Label Price;
        private Label Cantidad;
        private Label labelNoIva;
        private Label labelConIva;
        private CheckBox chkPartner;
    }
}
