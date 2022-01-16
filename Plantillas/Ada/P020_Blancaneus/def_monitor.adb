with Ada.Text_IO;              use Ada.Text_IO;

package body def_monitor is

   protected body monitor_sincro is

      --Return numero de enanos durmiendo
      function getADormir return Natural is
      begin
         return aDormir;
      end getADormir;

      --Return numero que piden comer
      function getPerMenjar return Natural is
      begin
         return perMenjar;
      end getPerMenjar;

      --Blancanieves: Dar de comer a un enano
      procedure donaMenjar is
      begin
         plats := plats + 1;
         perMenjar := perMenjar - 1;
         Put_Line("perMenjar =  " & perMenjar'Img & " cadires = " & cadires'Img);
      end;

      --Enanos: Pedir para senterse
      entry demanaCadira when cadires /= 0 is
      begin
         cadires := cadires - 1;
         perMenjar := perMenjar + 1;
      end;

      --Enanos: Pedir para comer ser servido
      entry demanaMenjar when plats /= 0 is --Si blancanieves a cocinado un plato
      begin
         plats := plats - 1;  --Se come el plato
      end;

      --Enanos: El enano se va
      procedure senVa is
      begin
         cadires := cadires + 1;
      end senVa;

      --Enanos: El enano se va a dormir
      procedure incrementaADormir is
      begin
         aDormir := aDormir + 1;
      end incrementaADormir;

   end monitor_sincro;

end def_monitor;
