AC_PREREQ([2.65])

AC_INIT([sltv], [0.3], [sltv-dev@listas.softwarelivre.org])

AC_CONFIG_MACRO_DIR([m4])

AC_CONFIG_SRCDIR([configure.ac])

AC_PROG_INSTALL

AM_INIT_AUTOMAKE([-Wall -Werror])

AM_PATH_PYTHON(2.4.0)

dnl expanding useful variables
AS_AC_EXPAND(LIBDIR, $libdir)
AS_AC_EXPAND(BINDIR, $bindir)
AS_AC_EXPAND(DATADIR, $datarootdir)

AC_CONFIG_FILES([
        Makefile
        sltv/ui/Makefile
	sltv/ui/input/Makefile
	sltv/input/Makefile
        sltv/Makefile
        sltv/sltv
        sltv/settings.py
])

AC_OUTPUT
