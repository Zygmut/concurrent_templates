with Ada.Text_IO;              use Ada.Text_IO;
with Ada.Strings.Unbounded;    use Ada.Strings.Unbounded;
with Ada.Text_IO.Unbounded_IO; use Ada.Text_IO.Unbounded_IO;
with Ada.Task_Identification;  use Ada.Task_Identification;

with def_monitor;              use def_monitor;

procedure Blancaneusinans is

   Nre_Nans           : constant := 7;
   Retard_Menjar      : constant := 0.5;
   Retard_Cuinar      : constant := 0.5;
   Retard_Passejar    : constant := 0.5;
   Fitxer_Personatges : constant String := "personatges.txt";


   monitor    : monitor_sincro;

   task type tasca_blancaneus is
      entry Start (Nom_Personatge : in Unbounded_String);
   end Tasca_Blancaneus;

   task body tasca_blancaneus is

      Nom : Unbounded_String;

   begin
      accept Start (Nom_Personatge : in Unbounded_String) do
         Nom := Nom_Personatge;
      end Start;
      Put_Line("BON DIA som na " & Nom);
      while monitor.getaDormir < Nre_Nans loop
         if (monitor.getPerMenjar = 0) then
            Put_Line("Blancaneus se'n va a fer una passejada ");
            delay Retard_Passejar;
         else
            Put_Line("Blancaneus cuina per un nan");
            delay Retard_Cuinar;
            Put_Line("Blancaneus té el menjat cuit");
            delay 0.1;
            monitor.donaMenjar;
         end if;
      end loop;
      Put_Line("Blancaneus s'en va a DORMIR " & monitor.getaDormir'Img );

   end tasca_blancaneus;

   task type tasca_nan is
      entry Start (Nom_Personatge : in Unbounded_String);
   end Tasca_Nan;

   task body tasca_nan is

      Nre_Menjades       : constant := 2;
      Retard_Treballar   : constant := 4.0;

      Nom     : Unbounded_String;

   begin
      accept Start (Nom_Personatge : in Unbounded_String) do
         Nom := Nom_Personatge;
      end Start;
      Put_Line("BON DIA som en " & Nom);
      for I in Positive range Positive'First .. Nre_Menjades loop
         Put_Line(Nom & " treballa a la mina");
         delay Retard_Treballar;
         Put_Line(Nom & " espera per una cadira");
         monitor.demanaCadira;
         Put_Line(Nom & " ja seu");
         Put_Line(Nom & " espera torn per menjar");
         monitor.demanaMenjar;
         Put_Line("----------------> " & Nom & " menja!!!");
         monitor.senVa;
      end loop;
      monitor.incrementaADormir;
      Put_Line(Nom & " se'n va a DORMIR " & monitor.getaDormir'Img & "/7");

   end tasca_nan;

   subtype Index_Noms is Positive range Positive'First .. 1 + Nre_Nans;
   type Array_Noms is array (Index_Noms) of Unbounded_String;
   subtype Index_Nan is Positive range Positive'First .. Nre_Nans;
   type Nans is array (Index_Nan) of tasca_nan;

   F          : File_Type;
   Noms       : Array_Noms;
   Blancaneus : tasca_blancaneus;
   Nan        : Nans;


begin
   Open(F, In_File, Fitxer_Personatges);
   for I in Noms'Range loop
      Noms(I) := To_Unbounded_String(Get_Line(F));
   end loop;
   Close(F);
   Blancaneus.Start(Noms(Array_Noms'First));
   for I in Nans'Range loop
      Nan(I).Start(Noms(Array_Noms'First + I));
   end loop;

--  exception
--
--     when Name_Error =>
--        Put_Line("No s'ha trobat el fitxer '" & Fitxer_Personatges & "'.");
--        Put_Line("Avortant...");
--
--        -- Avortam la tasca mestra,
--        -- aix� totes les tasques que depenen d'ella tamb� avortar�n
--
--        Abort_Task(Current_Task);
--
--     when End_Error =>
--        Put_Line("S'ha detectat un intent de sobrepassar el fi de fitxer.");
--        Put_Line("Avortant...");
--
--        -- Avortam la tasca mestra,
--        -- aix� totes les tasques que depenen d'ella tamb� avortar�n
--
--        Abort_Task(Current_Task);

end Blancaneusinans;
