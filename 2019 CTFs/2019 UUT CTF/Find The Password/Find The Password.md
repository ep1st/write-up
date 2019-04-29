# **Find The Password**

#### tag : reversing, .net

-----------------------------------------------

#### Description

>> Run the application and find the password.Run the application and find the password.

-----------------------------------------------

#### Solution

This is `Button1_Click` class which is for submit button. I can find md5 hashed password here. Hash value of password is `d1e48b836b862e8e7cf834b895ffc0de`.

~~~
  .method private hidebysig instance void Button1_Click(object sender, class [mscorlib]System.EventArgs e)
                                        // DATA XREF: UUTCTF_FindThePassword.Form1__InitializeComponent+1C2↓r
  {
    .maxstack 2
    .locals init (bool V0,
                  class UUTCTF_FindThePassword.Form2 V1)
    nop
    ldarg.0
    ldarg.0
    ldfld    class [System.Windows.Forms]System.Windows.Forms.TextBox UUTCTF_FindThePassword.Form1::textBox1
    callvirt instance string [System.Windows.Forms]System.Windows.Forms.Control::get_Text()
    call     instance string UUTCTF_FindThePassword.Form1::CalculateMD5Hash(string input)
    callvirt instance string [mscorlib]System.String::ToLower()
    ldstr    aD1e48b836b862e            // "d1e48b836b862e8e7cf834b895ffc0de"
    call     bool [mscorlib]System.String::op_Equality(string, string)
    stloc.0
    ldloc.0
    brfalse.s loc_66
    nop
    newobj   instance void UUTCTF_FindThePassword.Form2::.ctor()
    stloc.1
    ldloc.1
    callvirt instance valuetype [System.Windows.Forms]System.Windows.Forms.DialogResult [System.Windows.Forms]System.Windows.Forms.Form::ShowDialog()
    pop
    nop
    br.s     loc_73
loc_66:                                 // CODE XREF: UUTCTF_FindThePassword.Form1__Button1_Click+23↑j
    nop
    ldstr    aWrongPassword             // "Wrong Password."
    call     valuetype [System.Windows.Forms]System.Windows.Forms.DialogResult [System.Windows.Forms]System.Windows.Forms.MessageBox::Show(string)
    pop
    nop

~~~

`123456UUTctf` is raw string for `d1e48b836b862e8e7cf834b895ffc0d`. So password is `123456UUTctf`. And I can receive flag as `UUTCTF{sha1(Y0u_h4v3_f0uNd_coRr3Ct_FL4G)}` which is `UUTCTF{6dee35b953027debe077e05bbe7e488f8ab335c4}`. 

**UUTCTF{6dee35b953027debe077e05bbe7e488f8ab335c4}**
