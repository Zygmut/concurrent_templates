package def_monitor is

   protected type monitor_sincro is

      function getADormir return Natural;    --Return numero de enanos durmiendo
      function getPerMenjar return natural;  --Return numero que piden comer
      procedure donaMenjar;                  --Dar de comer a un enano
      entry demanaCadira;                    --Enano pide silla, "Lock" del proceso en el monitor
      entry demanaMenjar;                    --Enano pide comer, "Lock" del proceso en el monitor
      procedure senVa;                       --El enano se va
      procedure incrementaADormir;           --Enano se va a dormir "UnLock"

   private

      aDormir : Natural := 0;
      perMenjar : Natural := 0;
      cadires : Natural := 4;
      plats : Natural := 0;

   end monitor_sincro;

end def_monitor;
