with Ada.Text_IO;              use Ada.Text_IO;

package body def_monitor is

   protected body monitor_sincro is

      function getADormir return Natural is
      begin
         return aDormir;
      end getADormir;

      function getPerMenjar return Natural is
      begin
         return perMenjar;
      end getPerMenjar;

      procedure donaMenjar is
      begin
         plats := plats + 1;
         perMenjar := perMenjar - 1;
         Put_Line("perMenjar =  " & perMenjar'Img & " cadires = " & cadires'Img);
      end;

      entry demanaCadira when cadires /= 0 is
      begin
         cadires := cadires - 1;
         perMenjar := perMenjar + 1;
      end;

      entry demanaMenjar when plats /= 0 is
      begin
         plats := plats - 1;
      end;

      procedure senVa is
      begin
         cadires := cadires + 1;
      end senVa;

      procedure incrementaADormir is
      begin
         aDormir := aDormir + 1;
      end incrementaADormir;

   end monitor_sincro;

end def_monitor;
