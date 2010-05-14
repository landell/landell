AC_PREREQ([2.61])

AC_INIT([sltv], [0.7], [sltv-dev@listas.softwarelivre.org])

AC_CONFIG_MACRO_DIR([m4])

AC_CONFIG_SRCDIR([configure.ac])

AC_PROG_INSTALL

AM_INIT_AUTOMAKE([-Wall -Werror])

AM_PATH_PYTHON(2.5.0)

dnl expanding useful variables
AS_AC_EXPAND(LIBDIR, $libdir)
AS_AC_EXPAND(BINDIR, $bindir)
AS_AC_EXPAND(DATADIR, $datarootdir)

AC_CONFIG_FILES([
    Makefile
    ui/Makefile
    ui/input/Makefile
    ui/output/Makefile
    ui/encoding/Makefile
    sltv/input/Makefile
    sltv/output/Makefile
    sltv/encoding/Makefile
    sltv/effect/Makefile
    sltv/ui/Makefile
    sltv/ui/input/Makefile
    sltv/ui/output/Makefile
    sltv/ui/encoding/Makefile
    sltv/Makefile
    sltv/settings.py
    src/Makefile
    src/sltv
    man/Makefile
    sltv.desktop
])

AC_OUTPUT
