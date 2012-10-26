AC_PREREQ([2.61])

AC_INIT([landell], [0.92], [sltv-dev@listas.softwarelivre.org])

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
    landell/input/Makefile
    landell/output/Makefile
    landell/encoding/Makefile
    landell/effect/Makefile
    landell/ui/Makefile
    landell/ui/input/Makefile
    landell/ui/output/Makefile
    landell/ui/encoding/Makefile
    landell/Makefile
    landell/settings.py
    src/Makefile
    src/landell
    man/Makefile
    landell.desktop
])

AC_OUTPUT
