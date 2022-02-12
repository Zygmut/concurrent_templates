package def_monitor is

   protected type monitor_sincro is

      function getADormir return Natural;
      function getPerMenjar return natural;
      procedure donaMenjar;
      entry demanaCadira;
      entry demanaMenjar;
      procedure senVa;
      procedure incrementaADormir;

   private

      aDormir : Natural := 0;
      perMenjar : Natural := 0;
      cadires : Natural := 4;
      plats : Natural := 0;

      Nre_Cadires      : Natural  := 4;
      Nans_Adormits    : Natural  := 0;
      Nans_Afamats     : Natural  := 0;
      Plats_Preparats  : Natural  := 0;
      Cadires_Ocupades : Natural  := 0;

   end monitor_sincro;

end def_monitor;
